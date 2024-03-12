from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import settings
from fastapi import UploadFile
from app.schemas import messages as msg_schema


class EmailHandler:

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )

    fm = FastMail(conf)

    @classmethod
    async def send_message(
        cls,
        emails: list | str,
        subject: str,
        body: str,
        attachments: list[UploadFile] = [],
    ) -> None:
        message = MessageSchema(
            subject=subject,
            recipients=[emails] if isinstance(emails, str) else emails,
            body=body,
            attachments=attachments,
            subtype=MessageType.html,
        )

        await cls.fm.send_message(message)

        return msg_schema.MessageSchema(message="Сообщение успешно отправлено на почту")
