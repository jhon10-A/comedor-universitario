# Requisitos - Sistema de Comedor Universitario UNAMBA

Versión: v1.0

Fuente: Caso_practico.pdf del docente, páginas 1 y 2. Se conservan los códigos, el alcance, las prioridades, las categorías y las condiciones del documento. Se corrigen únicamente errores ortográficos evidentes para facilitar la lectura.

## Requerimientos funcionales

| Código | Descripción | Prioridad |
| --- | --- | --- |
| RF1 | Registrar e iniciar sesión de estudiantes. | Alta |
| RF2 | Gestionar beneficiarios, distinguiendo becarios y no becarios. | Alta |
| RF3 | Publicar el menú diario y semanal. | Alta |
| RF4 | Reservar una ración en un turno y horario. | Alta |
| RF5 | Controlar el aforo máximo por turno. | Alta |
| RF6 | Calcular la tarifa según la configuración del usuario y registro de pago. | Alta |
| RF7 | Emitir un ticket con código QR. | Mediana |
| RF8 | Validar el ingreso (QR o código de estudiante) y marcar el ticket como usado. | Alta |
| RF9 | Cancelar o reprogramar una reserva con anticipación mínima. | Mediana |
| RF10 | Gestionar el inventario de insumos y alertar sobre stock mínimo. | Mediana |
| RF11 | Generar reportes de raciones servidas, ingresos, asistencia y merma. | Medina (según el PDF) |
| RF12 | Enviar notificaciones sobre el menú y los cambios. | Baja |
| RF13 | Registrar sugerencias, quejas y encuestas de satisfacción. | Baja |

**Nota sobre RF11:** el PDF consigna literalmente la prioridad «Medina». Se conserva esa denominación, pendiente de aclaración del docente.

## Requerimientos no funcionales

| Código | Categoría | Requerimiento y condiciones |
| --- | --- | --- |
| RNF1 | Rendimiento | Respuesta en 2 segundos o menos con 500 usuarios simultáneos en hora pico. |
| RNF2 | Disponibilidad | Disponibilidad del 99% durante el horario de atención. |
| RNF3 | Seguridad | Contraseña cifrada, control de acceso por roles y conexión HTTPS. |
| RNF4 | Usabilidad | Interfaz simple y adaptable a celular, que se aprenda en 10 minutos. |
| RNF5 | Escalabilidad | Soportar más turnos. |
| RNF6 | Mantenibilidad | Código modular, pruebas unitarias y control de versiones con Git. |
| RNF7 | Compatibilidad | Compatibilidad con navegadores actuales, Android e iOS. |
| RNF8 | Integridad | Copia de seguridad diaria de la base de datos. |
| RNF9 | Privacidad | Cumplir la ley de protección de datos personales: ISO 17001, ley 29733, según lo indicado en el PDF. |

**Nota sobre RNF9:** las referencias «ISO 17001» y «ley 29733» se reproducen tal como aparecen en el caso práctico; su inclusión documenta el requisito del docente y no constituye una validación de esas referencias.
