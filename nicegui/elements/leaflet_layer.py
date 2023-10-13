from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Optional

from ..helpers import KWONLY_SLOTS

if TYPE_CHECKING:
    from .leaflet import Leaflet


@dataclass(**KWONLY_SLOTS)
class Layer:
    current_leaflet: ClassVar[Optional['Leaflet']] = None
    leaflet: 'Leaflet' = field(init=False)

    def __post_init__(self) -> None:
        self.leaflet = self.current_leaflet
        self.leaflet.layers.append(self)
        self.leaflet.run_method('add_layer', self.to_dict())

    @abstractmethod
    def to_dict(self) -> dict:
        pass