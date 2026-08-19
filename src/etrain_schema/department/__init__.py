"""Department-level analytics and reporting schemas."""

from .analysis import DepartmentAnalysis
from .graded import GradedIRTDepartmentAnalysis, GradedIRTDepartmentReport
from .report import DepartmentReport

__all__ = [
    "DepartmentAnalysis",
    "DepartmentReport",
    "GradedIRTDepartmentAnalysis",
    "GradedIRTDepartmentReport",
]
