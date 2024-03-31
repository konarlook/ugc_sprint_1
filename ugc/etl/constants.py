from models import (
    PlayerProgressEventSchema,
    PlayerSettingsEventSchema,
    ClickEventSchema
)

ASSOCIATION_TOPIC_TO_SCHEMA = {
        'player_progress': PlayerProgressEventSchema,
        'player_settings_event': PlayerSettingsEventSchema,
        'click_event': ClickEventSchema
    }