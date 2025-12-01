import json
import subprocess
import os
import sys
import uuid
import shutil
import io
from contextlib import redirect_stdout, redirect_stderr

def lambda_handler(event, context):
    try:
        # Manejo flexible del body para diferentes formatos de event
        body = None
        
        # Caso 1: event tiene 'body' (API Gateway)
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    return {
                        "statusCode": 400,
                        "body": json.dumps({
                            "stdout": "",
                            "stderr": "El body no es un JSON válido",
                            "return_code": 1
                        })
                    }
        # Caso 2: event es directamente el body (invocación directa)
        elif 'code' in event and 'test' in event:
            body = event
        # Caso 3: body vacío
        else:
            body = {}
    
        code = body.get('code', '') if body else ''
        test = body.get('test', '') if body else ''
        
        if not code:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "stdout": "",
                    "stderr": "No se proporcionó código para ejecutar",
                    "return_code": 1
                })
            }
        
        if not test:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "stdout": "",
                    "stderr": "No se proporcionó test para ejecutar",
                    "return_code": 1
                })
            }
        
        # Crear un directorio único para esta ejecución
        execution_id = str(uuid.uuid4())
        work_dir = os.path.join('/tmp', f'execution_{execution_id}')
        os.makedirs(work_dir, exist_ok=True)
        
        # Guardar el directorio de trabajo actual
        original_cwd = os.getcwd()
        
        try:
            # Crear archivos con nombres específicos directamente
            app_file_path = os.path.join(work_dir, 'app.py')
            test_file_path = os.path.join(work_dir, 'test_code.py')
            
            # Escribir el código del usuario
            with open(app_file_path, 'w') as app_file:
                app_file.write(code)
            
            # Escribir el test
            with open(test_file_path, 'w') as test_file:
                test_file.write(test)
            
            # Cambiar al directorio de trabajo
            os.chdir(work_dir)
            
            # Agregar el directorio de trabajo al path
            sys.path.insert(0, work_dir)
            
            # Limpiar cualquier módulo previamente importado que pueda interferir
            # Esto es importante porque Lambda reutiliza el entorno
            modules_to_remove = [mod for mod in sys.modules.keys() if mod.startswith('app') or mod.startswith('test_code')]
            for mod in modules_to_remove:
                del sys.modules[mod]
            
            # Desactivar la escritura de archivos .pyc
            sys.dont_write_bytecode = True
            
            # Importar pytest aquí para asegurar que se use la versión de la layer
            import pytest
            
            # Definir el plugin de pytest
            class FormatterPlugin:
                """
                Plugin de Pytest para capturar resultados y formatear
                la salida según los requisitos.
                """
                def __init__(self):
                    self.passed = 0
                    self.failed = 0
                    self.total = 0
                    self.failed_test_names = []
                    self.collection_error_messages = []

                def pytest_collectreport(self, report):
                    """
                    Hook #1: Se llama cuando pytest intenta 'recolectar' (importar)
                    un archivo de test.
                    """
                    if report.failed:
                        error_text = str(report.longrepr)
                        import_error_prefix = "ImportError: cannot import name '"
                        
                        if import_error_prefix in error_text:
                            try:
                                start_index = error_text.find(import_error_prefix) + len(import_error_prefix)
                                end_index = error_text.find("'", start_index)
                                    
                                if end_index != -1:
                                    function_name = error_text[start_index:end_index]
                                    self.collection_error_messages.append(f"No se encuentra la función '{function_name}' en el código")
                                else:
                                    self.collection_error_messages.append(f"Error de importación: {error_text.splitlines()[-1]}")  
                            except Exception:
                                self.collection_error_messages.append(f"Error de importación: {error_text.splitlines()[-1]}")
                        else:
                            self.collection_error_messages.append(f"Se ha encontrado el siguiente error en el codigo, porfavor corregir antes de correr los tests: {error_text.splitlines()[-1]}")

                def pytest_collection_finish(self, session):
                    """
                    Hook #3: Se llama después de que pytest ha terminado de 
                    encontrar todos los tests.
                    """
                    # Guardamos el número total de tests que encontró
                    self.total = len(session.items)

                def pytest_runtest_logreport(self, report):
                    """
                    Hook #2: Se llama después de que un test se ejecuta.
                    """
                    if report.when == 'call':
                        if report.passed:
                            self.passed += 1
                        elif report.failed:
                            self.failed += 1
                            test_name = report.nodeid.removeprefix("test_code.py::")
                            
                            error_text = str(report.longrepr)
                            name_error_prefix = "NameError: name '"
                            if name_error_prefix in error_text:
                                try:
                                    start = error_text.find(name_error_prefix) + len(name_error_prefix)
                                    end = error_text.find("'", start)
                                    name = error_text[start:end]

                                    message = f"{test_name} -> [Test no implementado correctamente]: La funcion '{name}' no existe. Porfavor contacte con su docente."
                                    self.failed_test_names.append(message)
                                except Exception:
                                    self.failed_test_names.append(f"{report.nodeid} (Error: NameError no parseable)")
                            else:
                                self.failed_test_names.append(test_name)
            
            # Crear instancia del plugin
            plugin = FormatterPlugin()
            
            # Capturar la salida de pytest
            output_buffer = io.StringIO()
            
            try:
                with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
                    # Ejecutar pytest sin buscar en otros directorios
                    pytest.main([
                        'test_code.py',
                        '-v',
                        '--tb=short',  # Traceback corto
                        '-p', 'no:cacheprovider',  # Desactivar caché de pytest
                        '--override-ini=python_files=test_code.py',  # Solo este archivo
                        '--override-ini=python_classes=',  # No buscar clases
                        '--override-ini=python_functions=test_*'  # Solo funciones test_*
                    ], plugins=[plugin])
                
                # Construir la salida formateada
                output_lines = []
                
                if plugin.collection_error_messages:
                    output_lines.append("\n[Errores encontrados al verificar el código]")
                    for message in plugin.collection_error_messages:
                        output_lines.append(f"  > {message}")
                    output = "\n".join(output_lines)
                    return_code = 1
                elif plugin.total == 0:
                    output = "\n[ADVERTENCIA]: No se han programado tests para esta actividad."
                    return_code = 2
                else:
                    output_lines.append(f"\nTests Superados: {plugin.passed}")
                    output_lines.append(f"Tests no superados: {plugin.failed}")
                    output_lines.append(f"Tests Totales: {plugin.total}")
                    
                    if plugin.failed_test_names:
                        output_lines.append("\nTests que no pasaron:")
                        for name in plugin.failed_test_names:
                            output_lines.append(f"  - {name}")
                    
                    output_lines.append(f"\nPuntaje obtenido: {int(plugin.passed / plugin.total * 100)}%")
                    output = "\n".join(output_lines)
                    return_code = 0 if plugin.failed == 0 else 1
                
                errors = ""
                
            except Exception as e:
                output = ""
                errors = f"Error al ejecutar pytest: {str(e)}"
                return_code = 1
        
        finally:
            # Restaurar sys.dont_write_bytecode
            sys.dont_write_bytecode = False
            
            # Restaurar el directorio de trabajo original
            os.chdir(original_cwd)
            
            # Limpiar el path
            if work_dir in sys.path:
                sys.path.remove(work_dir)
            
            # Limpiar módulos importados de esta ejecución
            modules_to_remove = [mod for mod in sys.modules.keys() if mod.startswith('app') or mod.startswith('test_code')]
            for mod in modules_to_remove:
                try:
                    del sys.modules[mod]
                except:
                    pass
            
            # Limpiar todo el directorio de ejecución
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir, ignore_errors=True)
        
        # Determinar el statusCode basado en el resultado de la ejecución
        status_code = 200 if return_code == 0 else 400
        
        return {
            "statusCode": status_code,
            "body": json.dumps({
                "stdout": output,
                "stderr": errors,
                "return_code": return_code
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "stdout": "",
                "stderr": f"Error en la función Lambda: {str(e)}",
                "return_code": 1
            })
        }
