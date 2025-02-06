from updateCitation import CitationNexus, projectURLTargets
from packaging.metadata import Metadata as PyPAMetadata
from typing import Any, Dict
import packaging
import packaging.metadata
import packaging.utils
import packaging.version

def getPyPAMetadata(packageData: Dict[str, Any]) -> PyPAMetadata:
    """
    Create a PyPA metadata object (version 2.4) from packageData.
    https://packaging.python.org/en/latest/specifications/core-metadata/
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

    metadata: PyPAMetadata = getPyPAMetadata(tomlPackageData)

    if not metadata.name:
        raise ValueError("Metadata name is required.")

    nexusCitation.title = metadata.name
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

    nexusCitation = nexusCitation.setInStone("PyPA")
    return nexusCitation
