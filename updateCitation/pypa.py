from updateCitation import CitationNexus, projectURLTargets
from packaging.metadata import Metadata as PyPAMetadata
from typing import Any, Dict
import packaging
import packaging.metadata
import packaging.utils
import packaging.version

def getPyPAMetadata(packageData: Dict[str, Any]) -> PyPAMetadata:
    """
    Retrieves and formats package metadata from a dictionary into a PyPAMetadata object.
    Parameters:
        packageData (Dict[str, Any]): A dictionary containing package information,
            typically obtained from an external source like a package index.
            It should include keys such as "name", "version", "keywords", "license",
            and "urls". The "urls" key should map to a dictionary where keys are
            URL names (e.g., "Homepage", "Documentation") and values are the
            corresponding URLs. The "license" key is expected to be a dictionary
            with a "text" key holding the license text.
    Returns:
        PyPAMetadata: A PyPAMetadata object containing the extracted and formatted
            metadata. The project URLs are filtered to include only those with keys
            present in the `projectURLTargets` set (converted to lowercase for
            comparison). The package name is canonicalized using
            `packaging.utils.canonicalize_name` and validated.
    Raises:
        packaging.metadata.InvalidMetadata: If the package name is missing from
            the input `packageData`. This exception is raised by
            `packaging.utils.canonicalize_name` if `validate=True` and the name
            is None. Other potential exceptions from `packaging.utils.canonicalize_name`
            are not explicitly handled.
    """
    dictionaryProjectURLs: Dict[str, str] = {}
    for urlName, url in packageData.get("urls", {}).items():
        urlName = urlName.lower()
        if urlName in projectURLTargets:
            dictionaryProjectURLs[urlName] = url

    metadataRaw = packaging.metadata.RawMetadata(
        keywords=packageData.get("keywords", []),
        license_expression=packageData.get("license", {}).get("text", ""),
        metadata_version="2.4",
        name=packaging.utils.canonicalize_name(packageData.get("name", None), validate=True), # packaging.metadata.InvalidMetadata: 'name' is a required field
        project_urls=dictionaryProjectURLs,
        version=packageData.get("version", None),
    )

    metadata = PyPAMetadata().from_raw(metadataRaw)
    return metadata

def addPyPAMetadata(nexusCitation: CitationNexus, tomlPackageData: Dict[str, Any]) -> CitationNexus:
    """Adds PyPA (Python Packaging Authority) metadata to a CitationNexus object.
        Parameters:
            nexusCitation (CitationNexus): The CitationNexus object to update.
            tomlPackageData (Dict[str, Any]): A dictionary containing the parsed TOML data
                from the package's pyproject.toml file.  This should contain the
                `project` table as specified in PEP 621.
        Returns:
            CitationNexus: The updated CitationNexus object with PyPA metadata.
        Raises:
            ValueError: If the metadata name is missing from the TOML data.
        """

    metadata: PyPAMetadata = getPyPAMetadata(tomlPackageData)

    if metadata.version: nexusCitation.version = str(metadata.version)
    if metadata.keywords: nexusCitation.keywords = metadata.keywords
    if metadata.license_expression: nexusCitation.license = metadata.license_expression

    Z0Z_lookup: Dict[str, str] = {
        "homepage": "url",
        "license": "licenseDASHurl",
        "repository": "repository",
    }
    if metadata.project_urls:
        for urlTarget in projectURLTargets:
            url = metadata.project_urls.get(urlTarget, None)
            if url:
                setattr(nexusCitation, Z0Z_lookup[urlTarget], url)

    nexusCitation.setInStone("PyPA")
    return nexusCitation
