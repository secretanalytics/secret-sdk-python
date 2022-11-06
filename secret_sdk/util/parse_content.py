from typing import Union

from secret_sdk.protobuf.cosmos.distribution.v1beta1 import (
    CommunityPoolSpendProposal as CommunityPoolSpendProposal_pb,
)
from secret_sdk.protobuf.cosmos.gov.v1beta1 import TextProposal as TextProposal_pb
from secret_sdk.protobuf.cosmos.params.v1beta1 import (
    ParameterChangeProposal as ParameterChangeProposal_pb,
)
from secret_sdk.protobuf.cosmos.upgrade.v1beta1 import (
    CancelSoftwareUpgradeProposal as CancelSoftwareUpgradeProposal_pb,
)
from secret_sdk.protobuf.cosmos.upgrade.v1beta1 import (
    SoftwareUpgradeProposal as SoftwareUpgradeProposal_pb,
)
from secret_sdk.protobuf.ibc.core.client.v1 import (
    ClientUpdateProposal as ClientUpdateProposal_pb,
)

from secret_sdk.core.distribution.proposals import CommunityPoolSpendProposal
from secret_sdk.core.gov.proposals import TextProposal
from secret_sdk.core.ibc.proposals import ClientUpdateProposal
from secret_sdk.core.params.proposals import ParameterChangeProposal
from secret_sdk.core.upgrade import (
    CancelSoftwareUpgradeProposal,
    SoftwareUpgradeProposal,
)

from .base import create_demux, create_demux_proto, create_demux_unpack_any

Content = Union[
    TextProposal,
    CommunityPoolSpendProposal,
    ParameterChangeProposal,
    SoftwareUpgradeProposal,
    CancelSoftwareUpgradeProposal,
    ClientUpdateProposal,
]

parse_content = create_demux(
    [
        CommunityPoolSpendProposal,
        TextProposal,
        ParameterChangeProposal,
        SoftwareUpgradeProposal,
        CancelSoftwareUpgradeProposal,
        ClientUpdateProposal,
    ]
)

parse_content_proto = create_demux_proto(
    [
        CommunityPoolSpendProposal,
        TextProposal,
        ParameterChangeProposal,
        SoftwareUpgradeProposal,
        CancelSoftwareUpgradeProposal,
        ClientUpdateProposal,
    ]
)

parse_content_unpack_any = create_demux_unpack_any(
    [
        CommunityPoolSpendProposal,
        TextProposal,
        ParameterChangeProposal,
        SoftwareUpgradeProposal,
        CancelSoftwareUpgradeProposal,
        ClientUpdateProposal,
    ]
)

"""
parse_content_proto = create_demux_proto(
    [
        [CommunityPoolSpendProposal.type_url, CommunityPoolSpendProposal_pb],
        [TextProposal.type_url, TextProposal_pb],
        [ParameterChangeProposal.type_url, ParameterChangeProposal_pb],
        [SoftwareUpgradeProposal.type_url, SoftwareUpgradeProposal_pb],
        [CancelSoftwareUpgradeProposal.type_url, CancelSoftwareUpgradeProposal_pb],
        [ClientUpdateProposal.type_url, ClientUpdateProposal_pb]
    ]
)
"""
