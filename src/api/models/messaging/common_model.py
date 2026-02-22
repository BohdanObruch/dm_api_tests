from __future__ import annotations

from src.api.models.shared.base_model import (
    BadRequestError as SharedBadRequestError,
)
from src.api.models.shared.base_model import (
    GeneralError as SharedGeneralError,
)
from src.api.models.shared.base_model import (
    Paging as SharedPaging,
)
from src.api.models.shared.user_model import (
    BbParseMode as SharedBbParseMode,
)
from src.api.models.shared.user_model import (
    CommonBbText as SharedCommonBbText,
)
from src.api.models.shared.user_model import (
    Rating as SharedRating,
)
from src.api.models.shared.user_model import (
    User as SharedUser,
)
from src.api.models.shared.user_model import (
    UserRole as SharedUserRole,
)

Paging = SharedPaging
UserRole = SharedUserRole
BbParseMode = SharedBbParseMode
Rating = SharedRating
User = SharedUser
CommonBbText = SharedCommonBbText
GeneralError = SharedGeneralError
BadRequestError = SharedBadRequestError
