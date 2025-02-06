from .constants import GITHUB_API_VERSION_HEADER # CAPSLOCK != immutable
from .variables import CitationNexus, projectURLTargets, filenameCitationDOTcff

from .pyprojectDOTtoml import get_pyprojectDOTtoml, add_pyprojectDOTtoml
from .pypa import addPyPAMetadata
from .nexusCitation import getNexusCitation
from .github import addGitHubRelease
from .pypi import addPyPIrelease
