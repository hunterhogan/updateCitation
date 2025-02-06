from cffconvert.cli.create_citation import create_citation
from updateCitation import CitationNexus
from typing import Any, Dict, List
import attrs
import cffconvert
import pathlib

def getNexusCitation(pathFilenameCitationSSOT: pathlib.Path) -> CitationNexus:

    # `cffconvert.cli.create_citation.create_citation()` is PAINFULLY mundane, but a major problem
    # in the CFF ecosystem is divergence. Therefore, I will use this function so that my code
    # converges with the CFF ecosystem.
    citationObject: cffconvert.Citation = create_citation(infile=pathFilenameCitationSSOT, url=None)
    # `._parse()` is a yaml loader: use it for convergence
    cffobj: Dict[Any, Any] = citationObject._parse()

    nexusCitation = CitationNexus(
        cffDASHversion=cffobj["cff-version"],
        message=cffobj["message"],
    )

    Z0Z_list: List[attrs.Attribute] = list(attrs.fields(type(nexusCitation)))
    for Z0Z_field in Z0Z_list:
        cffobjKeyName: str = Z0Z_field.name.replace("DASH", "-")
        cffobjValue = cffobj.get(cffobjKeyName)
        if cffobjValue: # An empty list will be False
            setattr(nexusCitation, Z0Z_field.name, cffobjValue)

    nexusCitation = nexusCitation.setInStone("Citation")
    return nexusCitation
