from cffconvert.cli.create_citation import create_citation
from updateCitation import CitationNexus
from typing import Any, Dict, List
import attrs
import cffconvert
import pathlib

def addCitation(nexusCitation: CitationNexus, pathFilenameCitationSSOT: pathlib.Path) -> CitationNexus:
    """Given a path to a citation file, return a CitationNexus object.
        The citation file is expected to be in a format that can be parsed by
        `cffconvert.cli.create_citation.create_citation()`. This function
        ensures convergence with the CFF ecosystem by using `create_citation`
        and its internal `_parse()` method.
        Parameters:
            pathFilenameCitationSSOT (pathlib.Path): Path to the citation file.
        Returns:
            CitationNexus: A CitationNexus object populated with data from the
                citation file.
        """

    # `cffconvert.cli.create_citation.create_citation()` is PAINFULLY mundane, but a major problem
    # in the CFF ecosystem is divergence. Therefore, I will use this function so that my code
    # converges with the CFF ecosystem.
    citationObject: cffconvert.Citation = create_citation(infile=pathFilenameCitationSSOT, url=None)
    # `._parse()` is a yaml loader: use it for convergence
    cffobj: Dict[Any, Any] = citationObject._parse()

    # This step is designed to prevent deleting fields that are populated in the current CFF file,
    # but for whatever reason do not get added to the CitationNexus object.
    Z0Z_list: List[attrs.Attribute] = list(attrs.fields(type(nexusCitation)))
    for Z0Z_field in Z0Z_list:
        cffobjKeyName: str = Z0Z_field.name.replace("DASH", "-")
        cffobjValue = cffobj.get(cffobjKeyName)
        if cffobjValue: # An empty list will be False
            setattr(nexusCitation, Z0Z_field.name, cffobjValue)

    nexusCitation = nexusCitation.setInStone("Citation")
    return nexusCitation
