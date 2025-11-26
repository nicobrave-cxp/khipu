### **Guía de Implementación: Botón de Pago Khipu para WhatsApp (Versión Corregida y Detallada)**

Este documento sirve como referencia técnica para integrar el sistema de pagos de Khipu en un flujo de chat de WhatsApp. El objetivo es generar un enlace de pago dinámico, enviarlo a un usuario y confirmar la transacción de manera automática utilizando webhooks.

Esta guía ha sido actualizada para reflejar el flujo funcional de la **API de Pagos v3** de Khipu.

#### **Prerrequisitos**

1.  **Cuenta de Khipu:** Debes tener una cuenta de usuario en [khipu.com](https://khipu.com).
2.  **Cuenta de Cobro en Modo Desarrollador:** Dentro de tu perfil de Khipu, crea y activa una "cuenta de cobro". Es indispensable **activar el modo desarrollador** y usar una "cuenta de cobro de desarrollador" para las pruebas.
3.  **Plataforma de WhatsApp Business API:** Un proveedor de servicios para enviar y recibir mensajes de forma programática.
4.  **Servidor Backend:** Un servidor (ej. Node.js) capaz de alojar los webhooks y ser accesible desde Internet.

---

#### **Paso 1: Configuración de Credenciales y Entorno**

1.  **Obtener Credenciales de Khipu (API v3):**
    *   Ve a tu cuenta de cobro de desarrollador en Khipu.
    *   Busca la sección de integración para la **API de Pagos v3**.
    *   **Importante:** Asegúrate de que tu **Clave de API secreta (`x-api-key`)** corresponda a esta versión. Las claves de versiones anteriores no funcionarán y resultarán en un error `403 Forbidden`.

2.  **Crear Archivo `.env`:**
    *   En la raíz de tu proyecto, crea un archivo `.env` para almacenar tus credenciales de forma segura.

    ```dotenv
    # Credenciales de Khipu (para API v3)
    KHIPU_API_KEY="TU_X_API_KEY_SECRETA_V3"
    ```

---

#### **Paso 2: Webhook para Chat de WhatsApp (Receptor de Mensajes)**

Este paso es conceptual y no cambia. Tu servidor necesita un endpoint (ej. `/api/whatsapp/webhook`) para recibir mensajes de los usuarios, procesar sus solicitudes de pago y llamar a la lógica del Paso 3.

---

#### **Paso 3: Crear el Cobro en Khipu**

Esta es la comunicación central con Khipu para generar el enlace de pago.

1.  **Endpoint de Khipu:** `POST https://payment-api.khipu.com/v3/payments`

2.  **Cabeceras Requeridas:**
    *   `x-api-key`: Tu clave secreta obtenida del archivo `.env`.
    *   `Content-Type`: `application/json`

3.  **Cuerpo de la Petición (Request Body - JSON):**
    A continuación se detallan los campos enviados para crear el pago.
    *   `subject` (string, **requerido**): El motivo del cobro, que se mostrará al cliente. *Ej: "Factura #1234"*
    *   `amount` (number, **requerido**): El monto a cobrar, como un número entero o decimal. *Ej: 1500*
    *   `currency` (string, **requerido**): El código de la moneda en formato ISO-4217. *Ej: "CLP"*
    *   `transaction_id` (string, opcional): Un identificador único generado por tu sistema. Es **muy recomendado** para conciliar el pago después. *Ej: "ORDEN-654321"*
    *   `body` (string, opcional): Una descripción más detallada del cobro. *Ej: "Compra de 2 entradas para el cine."*
    *   `returnUrl` (string, opcional): URL a la que el usuario es redirigido tras un pago exitoso.
    *   `cancelUrl` (string, opcional): URL a la que el usuario es redirigido si cancela el pago.
    *   `notifyUrl` (string, opcional): URL de tu webhook que recibirá la notificación de pago. Si no se define aquí, se usará la configurada en el panel de Khipu.
    *   `expires_date` (string, opcional): Fecha y hora de expiración del cobro en formato ISO 8601.

4.  **Cuerpo de la Respuesta (Response Body - JSON):**
    Si la creación es exitosa, Khipu responderá con un objeto como el siguiente.
    *   `payment_id` (string): Identificador único del pago en Khipu.
    *   `payment_url` (string): La URL principal a la que debes redirigir al usuario para que realice el pago.
    *   `simplified_transfer_url` (string): URL para un flujo de pago simplificado.
    *   `transfer_url` (string): URL para un flujo de pago manual.
    *   `app_url` (string): URL para abrir el pago directamente en la aplicación móvil de Khipu.
    *   `ready_for_terminal` (boolean): Indica si el pago está listo para ser procesado en un terminal Khipu.

---

#### **Paso 4: Webhook para Confirmación de Pago de Khipu**

Este webhook es crucial para automatizar la confirmación.

1.  **Endpoint:** El que tú definas (ej. `/api/khipu/webhook`).

2.  **Petición de Khipu (Request Body - JSON):**
    Cuando un pago se completa, Khipu enviará un `POST` a tu endpoint con un cuerpo JSON detallado. A continuación se describen todos los campos recibidos en nuestra prueba.
    *   `payment_id` (string): El ID único del pago en Khipu.
    *   `receiver_id` (number): El ID de tu cuenta de cobro en Khipu.
    *   `subject` (string): El asunto del cobro que definiste.
    *   `amount` (string): El monto final pagado, como cadena de texto.
    *   `discount` (string): El monto del descuento aplicado, si lo hubiera.
    *   `currency` (string): La moneda del pago.
    *   `body` (string): La descripción detallada del cobro.
    *   `receipt_url` (string): Un enlace al comprobante del pago en formato PDF.
    *   `bank` (string): El nombre del banco utilizado por el pagador (en este caso, el banco de prueba).
    *   `bank_id` (string): El identificador del banco.
    *   `payer_name` (string): El nombre del titular de la cuenta que realizó el pago.
    *   `payer_email` (string): El correo electrónico del pagador.
    *   `personal_identifier` (string): El identificador personal (RUT en Chile) del pagador.
    *   `bank_account_number` (string): El número de la cuenta bancaria desde la que se pagó.
    *   `out_of_date_conciliation` (boolean): Indica si la conciliación se realizó fuera de tiempo.
    *   `transaction_id` (string): El ID que tú enviaste al crear el cobro, crucial para la conciliación.
    *   `responsible_user_email` (string): El correo del usuario responsable en la cuenta Khipu.
    *   `payment_method` (string): El método de pago utilizado (ej: "SIMPLIFIED_TRANSFER").
    *   `conciliation_date` (string): La fecha y hora en que Khipu concilió el pago, en formato ISO 8601.

    *   **Ejemplo de Notificación Recibida:**
        ```json
        {
          "payment_id": "r6uqukroeqbp",
          "receiver_id": 507709,
          "subject": "Producto de Prueba",
          "amount": "100.00",
          "discount": "0.00",
          "currency": "CLP",
          "body": "Descripción del producto de prueba",
          "receipt_url": "https://s3.amazonaws.com/notifications.khipu.com/CPKH-0511252054-r6uqukroeqbp.pdf",
          "bank": "DemoBank",
          "bank_id": "Bawdf",
          "payer_name": "Cobrador de desarrollo #507.709",
          "payer_email": "s.duarte@hotmail.es",
          "personal_identifier": "16786170-9",
          "bank_account_number": "814014940130",
          "out_of_date_conciliation": false,
          "transaction_id": "6810baa4-feb2-4fdc-8585-dd9a128e1278",
          "responsible_user_email": "lsduarteh@gmail.com",
          "payment_method": "SIMPLIFIED_TRANSFER",
          "conciliation_date": "2025-11-05T23:54:12.605Z"
        }
        ```
    *   **Actualizar Base de Datos:** Usa el `transaction_id` del JSON para buscar la orden en tu sistema y marcarla como pagada.
    *   **Responder a Khipu:** Responde siempre con un código de estado `HTTP 200 OK` para que Khipu sepa que recibiste la notificación y no intente reenviarla.