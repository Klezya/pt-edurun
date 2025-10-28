import pytest
import io
from contextlib import redirect_stdout, redirect_stderr

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
        

plugin = FormatterPlugin()
test_files = ['test_code.py']

f = io.StringIO()
with redirect_stdout(f), redirect_stderr(f):
    pytest.main(test_files, plugins=[plugin])

if plugin.collection_error_messages:
    print("\n[Errores encontrados al verificar el código]")
    for message in plugin.collection_error_messages:
        print(f"  > {message}")
    exit(1)

if plugin.total == 0 and not plugin.collection_error_messages:
    print("\n[ADVERTENCIA]: No se han programado tests para esta actividad.")
    exit(2)

print(f"\nTests Superados: {plugin.passed}")
print(f"Tests no superados: {plugin.failed}")
print(f"Tests Totales: {plugin.total}")

if plugin.failed_test_names:
    print("\nTests que no pasaron:")
    for name in plugin.failed_test_names:
        print(f"  - {name}")

if plugin.total > 0:
    print(f"\nPuntaje obtenido: {int(plugin.passed / plugin.total * 100)}%")