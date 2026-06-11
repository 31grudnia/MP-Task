from dataclasses import dataclass, field


@dataclass(frozen=True)
class PanelConfig:
    width: float = 44.7
    height: float = 71.1


@dataclass(frozen=True)
class RafterConfig:
    spacing: float = 16.0
    first_rafter_x: float = 0.0  


@dataclass(frozen=True)
class MountConfig:
    edge_clearance: float = 2.0     
    cantilever_limit: float = 16.0  
    span_limit: float = 48.0        


@dataclass(frozen=True)
class JointConfig:
    horizontal_gap_threshold: float = 1.0  
    vertical_gap_threshold: float = 1.0    
    max_shared_panels: int = 4             


@dataclass(frozen=True)
class Settings:
    panel: PanelConfig = field(default_factory=PanelConfig)
    rafter: RafterConfig = field(default_factory=RafterConfig)
    mount: MountConfig = field(default_factory=MountConfig)
    joint: JointConfig = field(default_factory=JointConfig)


DEFAULT_SETTINGS = Settings()