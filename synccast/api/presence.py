# Default package imports
from typing import Optional, Dict, Any, Union

# SyncCast abstract model
from synccast.models import AbstractSyncCastScope

# SyncCast builder
from synccast.core.topic import SyncCastTopicBuilder
from synccast.core.payload import SyncCastPayloadBuilder

# SyncCast service dispatcher
from synccast.core.dispatcher import SyncCastDispatcher

# SyncCast enums
from synccast.core.enums import SyncCastEventType

# SyncCast service endpoints
from synccast.core.endpoints import PushEndpoints
 
# SyncCast custom exceptions
from synccast.exceptions.types import (
    SyncCastTopicError,
    SyncCastPayloadError,
    SyncCastDispatchError,
    SyncCastAPIError
)


class PresenceService:
    """
    Service for dispatching presence status updates over SyncCast.
    """

    def __init__(self, dispatcher: SyncCastDispatcher, app_id: str):
        self.dispatcher = dispatcher
        self.app_id = app_id

    def send_presence(
        self,
        *,
        user_id: str,
        data: Dict[str, Any],
        scope: Union[str, AbstractSyncCastScope] = "chat",
        topic: Optional[str] = None,
        sender_name: Optional[str] = None,
        sender_role: Optional[str] = None,
        platform: Optional[str] = None,
        device: Optional[str] = None,
        location: Optional[str] = None,
    ) -> dict:
         
        try:

            # Build payload
            payload_builder = (
                SyncCastPayloadBuilder(user=user_id, type=SyncCastEventType.USER_PRESENCE)
                .set_scope(scope)
                .set_topic(topic)
                .set_data(data)
            )

            if sender_name:
                payload_builder.set_sender_info(sender_id=user_id, sender_name=sender_name, sender_role=sender_role)

            if platform or device or location:
                payload_builder.set_metadata(
                    platform or "unknown", device or "unknown", location or "unknown"
                )

            payload = payload_builder.build()

            # Dispatch to broker
            return self.dispatcher.post(PushEndpoints.PRESENCE, json=payload)

        except SyncCastPayloadError as e:
            raise SyncCastPayloadError(
                message="Invalid presence payload",
                extra={"user_id": user_id, "topic": topic}
            ) from e

        except SyncCastDispatchError:
            raise  # Already carries context from dispatcher

        except Exception as e:
            raise SyncCastAPIError(
                message="Unexpected error while sending presence update",
                extra={"user_id": user_id, "topic": topic, "error": str(e)}
            ) from e
