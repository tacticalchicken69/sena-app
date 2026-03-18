from django.test import TestCase, Client
from django.urls import reverse
from aprendices.models import Aprendiz
from aprendices.forms import AprendizForm
from django.db import IntegrityError
# Create your tests here.
""" --- Clase base reutilizable que crea un Aprendiz de prueba.
Heredar de esta clase evita duplicar el setUp en cada TestCase. --- """

class AprendizTestBase(TestCase):

    # setUp() se llama ANTES de cada método test_xxx.
    def setUp(self):
        # Creamos un aprendiz con datos válidos y conocidos.
        
        self.aprendiz = Aprendiz.objects.create(
            documento_identidad='1052838619',
            nombre='Andres',
            apellido='Gonzalez',
            telefono='3136332436',
            correo_electronico='andresgonzalez3900x@gmail.com',
            fecha_nacimiento='2006-08-01',
            ciudad='Sogamoso',
            programa='Análisis y Desarrollo de Software'
        )
        
        # Creamos un cliente HTTP para simular peticiones al servidor.
        self.client = Client()




""" --- Pruebas unitarias para el modelo Aprendiz.
Verificamos campos, métodos y restricciones de la BD. --- """

class AprendizModelTest(AprendizTestBase):

    # --- Test 1: Creación Aprendiz ---
    def test_aprendiz_se_crea_correctamente(self):
        # Usamos el documento exacto de tu base: '1052838619'
        aprendiz = Aprendiz.objects.get(documento_identidad='1052838619')
        self.assertEqual(aprendiz.nombre, 'Andres')
        self.assertEqual(aprendiz.apellido, 'Gonzalez')
        self.assertEqual(aprendiz.ciudad, 'Sogamoso')

  
  # --- Test 2: Método __str__ ---
    def test_str_retorna_nombre_y_apellido(self):
        self.assertEqual(str(self.aprendiz), 'Andres Gonzalez')

        # --- Test 3: Método nombre_completo() ---
    def test_nombre_completo_concatena_correctamente(self):
        self.assertEqual(self.aprendiz.nombre_completo(), 'Andres Gonzalez')

    # --- Test 4: Unicidad del documento ---
    def test_documento_identidad_debe_ser_unico(self):
        with self.assertRaises(IntegrityError):
            Aprendiz.objects.create(
                documento_identidad='1052838619',  # Mismo documento que Andres
                nombre='Otro',
                apellido='Usuario',
                fecha_nacimiento='2000-01-01',
                programa=self.aprendiz.programa # Usamos el mismo programa
            )

# --- Test 5: Campos opcionales permiten null ---
    def test_campos_opcionales_aceptan_null(self):
        # Creamos un aprendiz solo con los campos obligatorios
        aprendiz_minimo = Aprendiz.objects.create(
            documento_identidad='999999999',
            nombre='Maria',
            apellido='Gomez',
            fecha_nacimiento='2001-03-10',
            programa=self.aprendiz.programa
        )
        self.assertIsNone(aprendiz_minimo.telefono)
        self.assertIsNone(aprendiz_minimo.correo_electronico)
        self.assertIsNone(aprendiz_minimo.ciudad)


""" --- Pruebas para el formulario AprendizForm.
Probamos validaciones tanto positivas (datos correctos)
como negativas (datos incorrectos que deben ser rechazados). --- """

class AprendizFormTest(TestCase):
    def get_datos_validos(self):
        """Método auxiliar que retorna un diccionario con datos correctos."""
        return {
            'documento_identidad': '1098765432',
            'nombre': 'Laura',
            'apellido': 'García',
            'telefono': '3209876543',
            'correo_electronico': 'laura@sena.edu.co', # Corregido de 'correo'
            'fecha_nacimiento': '2002-07-20',
            'ciudad': 'Medellín',
        }

    # --- Test 1: Formulario válido ---
    def test_formulario_valido_con_datos_correctos(self):
        form = AprendizForm(data=self.get_datos_validos())
        self.assertTrue(form.is_valid(), msg=f'Errores: {form.errors}')

    # --- Test 2: Documento con letras ---
    def test_documento_con_letra_es_invalido(self):
        datos = self.get_datos_validos()
        datos['documento_identidad'] = 'ABC123456'
        form = AprendizForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('documento_identidad', form.errors)
        self.assertIn('solo números', str(form.errors['documento_identidad']))

    # --- Test 3: Teléfono con letras ---
    def test_telefono_con_letras_es_invalido(self):
        datos = self.get_datos_validos()
        datos['telefono'] = 'abc1234567'
        form = AprendizForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    # --- Test 4: Teléfono con longitud incorrecta ---
    def test_telefono_con_menos_de_10_digitos_es_invalido(self):
        datos = self.get_datos_validos()
        datos['telefono'] = '31012345'
        form = AprendizForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    # --- Test 5: Correo inválido ---
    def test_correo_invalido_es_rechazado(self):
        datos = self.get_datos_validos()
        datos['correo_electronico'] = 'esto_no_es_un_correo' # Corregido
        form = AprendizForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('correo_electronico', form.errors)

    # --- Test 6: Campos obligatorios vacíos ---
    def test_campos_obligatorios_vacios_invalidan_formulario(self):
        form = AprendizForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('documento_identidad', form.errors)
        self.assertIn('nombre', form.errors)
        self.assertIn('apellido', form.errors)

""" --- Pruebas de integración para las vistas del módulo aprendices.
Usamos self.client para simular peticiones HTTP reales. --- """

class AprendizViewsTest(AprendizTestBase):

    """ --- Tests de Vistas de Lectura (GET) --- """

    # --- Test 1: Lista de aprendices ---
    def test_lista_aprendices_responde_200(self):
        url = reverse('aprendices:lista_aprendices')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_lista_aprendices_usa_template_correcto(self):
        url = reverse('aprendices:lista_aprendices')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'lista_aprendices.html')

    def test_lista_aprendices_contiene_el_aprendiz_creado(self):
        url = reverse('aprendices:lista_aprendices')
        response = self.client.get(url)
        # Verificamos que se muestre Andres Gonzalez en el HTML
        self.assertContains(response, 'Andres')
        self.assertContains(response, 'Gonzalez')

    # --- Test 2: Detalle de aprendiz ---
    def test_detalle_aprendiz_existente_responde_200(self):
        url = reverse('aprendices:detalle_aprendiz', args=[self.aprendiz.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Verificamos que el documento de Andres sea visible
        self.assertContains(response, '1052838619')  

    """ --- Tests de Vistas de Escritura (POST) --- """

    # --- Test 3: Crear aprendiz (POST válido) ---
    def test_crear_aprendiz_con_datos_validos_redirige(self):
        url = reverse('aprendices:crear_aprendiz')
        datos = {
            'documento_identidad': '5555555555',
            'nombre': 'Carlos',
            'apellido': 'López',
            'telefono': '3001112233',
            'correo_electronico': 'carlos@test.com', # Corregido
            'fecha_nacimiento': '1999-11-05',
            'ciudad': 'Cali',
            'programa': 'Análisis y Desarrollo de Software' # Lo agregué por si el modelo lo pide
        }
        response = self.client.post(url, data=datos)
        # Después de crear exitosamente, debe redirigir a la lista
        self.assertEqual(response.status_code, 302)
        # Verificamos que el aprendiz realmente se guardó en la BD
        self.assertTrue(
            Aprendiz.objects.filter(documento_identidad='5555555555').exists()
        )

    def test_crear_aprendiz_con_datos_invalidos_no_redirige(self):
        url = reverse('aprendices:crear_aprendiz')
        datos_invalidos = {
            'documento_identidad': 'INVALIDO',  # tiene letras
            'nombre': '',                       # vacío
            'apellido': 'Test',
            'fecha_nacimiento': '2000-01-01',
        }
        response = self.client.post(url, data=datos_invalidos)
        # No redirige: vuelve al formulario con errores
        self.assertEqual(response.status_code, 200)
        # El aprendiz NO fue creado en la BD
        self.assertFalse(
            Aprendiz.objects.filter(documento_identidad='INVALIDO').exists()
        )

    # --- Test 4: Editar aprendiz ---
    def test_editar_aprendiz_actualiza_datos(self):
        url = reverse('aprendices:editar_aprendiz', args=[self.aprendiz.id])
        datos_actualizados = {
            'documento_identidad': '1052838619', # Usamos el ID original de Andres
            'nombre': 'Juan Carlos',             # nombre modificado
            'apellido': 'Gonzalez',
            'telefono': '3001234567',
            'correo_electronico': 'juan@test.com',
            'fecha_nacimiento': '2006-08-01',
            'ciudad': 'Barranquilla',            # ciudad modificada
            'programa': 'Análisis y Desarrollo de Software'
        }
        response = self.client.post(url, data=datos_actualizados)
        self.assertEqual(response.status_code, 302)
        # Refrescamos el objeto desde la BD
        self.aprendiz.refresh_from_db()
        # Verificamos que los datos cambiaron a lo que enviamos
        self.assertEqual(self.aprendiz.nombre, 'Juan Carlos')
        self.assertEqual(self.aprendiz.ciudad, 'Barranquilla')

    # --- Test 5: Eliminar aprendiz ---
    def test_eliminar_aprendiz_lo_borra_de_la_bd(self):
        aprendiz_id = self.aprendiz.id
        url = reverse('aprendices:eliminar_aprendiz', args=[aprendiz_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        # Verificamos que ya no existe en la BD
        self.assertFalse(
            Aprendiz.objects.filter(id=aprendiz_id).exists()
        )


        """ --- Tests de las URLS --- """

class AprendizURLTest(TestCase):
    # Nota: Como definiste app_name = 'aprendices', reverse usa el prefijo 'aprendices:'
    
    def test_url_lista_aprendices_resuelve_correctamente(self):
        url = reverse('aprendices:lista_aprendices')
        self.assertEqual(url, '/aprendices/')

    def test_url_crear_aprendiz_resuelve_correctamente(self):
        url = reverse('aprendices:crear_aprendiz')
        self.assertEqual(url, '/aprendices/crear/')

    def test_url_detalle_aprendiz_resuelve_correctamente(self):
        url = reverse('aprendices:detalle_aprendiz', args=[1])
        self.assertEqual(url, '/aprendices/1/')

    def test_url_editar_aprendiz_resuelve_correctamente(self):
        url = reverse('aprendices:editar_aprendiz', args=[1])
        self.assertEqual(url, '/aprendices/1/editar/')

    def test_url_eliminar_aprendiz_resuelve_correctamente(self):
        url = reverse('aprendices:eliminar_aprendiz', args=[1])
        self.assertEqual(url, '/aprendices/1/eliminar/')