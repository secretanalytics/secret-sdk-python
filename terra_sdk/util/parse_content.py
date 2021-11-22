from terra_sdk.core.distribution.proposals import CommunityPoolSpendProposal

from .base import create_demux

parse_content = create_demux(
    [
        CommunityPoolSpendProposal,
    ]
)
