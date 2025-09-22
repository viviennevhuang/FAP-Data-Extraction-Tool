from typing import Optional, List 
from pydantic import BaseModel, Field


class ReturnsPercentage(BaseModel):
    one_year: Optional[float] = Field(None, alias="1y")
    three_year: Optional[float] = Field(None, alias="3y")
    five_year: Optional[float] = Field(None, alias="5y")
    seven_year: Optional[float] = Field(None, alias="7y")
    ten_year: Optional[float] = Field(None, alias="10y")
    twenty_year: Optional[float] = Field(None, alias="20y")
    thirty_year: Optional[float] = Field(None, alias="30y")
    since_inception: Optional[float] = Field(None, alias="since_inception")
    metric_clarification: str 

class ReportPeriod(BaseModel):
    value: str
    clarification: str


class AssetAllocation(BaseModel):
    equities: Optional[float] = None
    fixed_income: Optional[float] = None
    alternatives: Optional[float] = None
    cash: Optional[float] = None
    total_percent: Optional[float] = None
    notes: Optional[str] = None

class Metric(BaseModel):
    value: Optional[float] = None
    time_period: Optional[str] = None
    metric_clarification: Optional[str] = None

class Metrics(BaseModel):
    sharpe_ratio: Optional[List[Metric]] = None
    internal_rate_of_return: Optional[List[Metric]] = None
    active_return: Optional[List[Metric]] = None
    volatility: Optional[List[Metric]] = None
    value_at_risk: Optional[List[Metric]] = None
    monte_carlo: Optional[List[Metric]] = None
    information_ratio: Optional[List[Metric]] = None
    ex_ante_tracking_error: Optional[List[Metric]] = None
    ex_post_tracking_error: Optional[List[Metric]] = None
    hit_ratio: Optional[List[Metric]] = None
    

class GeographicAllocation(BaseModel):
    north_america: Optional[float] = None
    europe: Optional[float] = None
    asia: Optional[float] = None
    latin_america: Optional[float] = None
    africa: Optional[float] = None
    oceania: Optional[float] = None
    developed: Optional[float] = None
    emerging: Optional[float] = None
    globally: Optional[float] = None
    other: Optional[float] = None
    total_percent: Optional[float] = None
    notes: Optional[str] = None


class Benchmarks(BaseModel):
    benchmark_name: str
    fund_return: float
    benchmark_return: Optional[float]
    time_period: str
    comparison_result: str
    metric_clarification: str
    comments_or_reasoning: Optional[str]

class AssetsUnderManagement(BaseModel):
    value: float
    currency: str

class ManagementCosts(BaseModel):
    management_fees: Optional[float] = None
    management_fees_currency: Optional[str] = None
    management_fees_percent_aum: Optional[float] = None
    notes: Optional[str] = None


class SWFReport(BaseModel):
    fund_name: str
    country: str
    reporting_period: ReportPeriod
    annual_return_percent: List[ReturnsPercentage]
    benchmark_comparison: Optional[List[Benchmarks]]
    investment_mandate: str
    investment_horizon: str
    metrics: Optional[Metrics]
    asset_allocation: AssetAllocation
    investment_geography: Optional[List[GeographicAllocation]]
    assets_under_management: Optional[AssetsUnderManagement]
    management_costs: Optional[ManagementCosts]
    notes: Optional[str]
