"""
Clients
    Company
        Name
    Campaigns
        Budget
        Revenue per sale
        Variable costs
        Goals
            Contribution Margin
            Client Acquisition cost
    Users
        Email, Pass

Oustanding:

How many candidates to get a potential hire?

How many hires to achieve break event?


"""

config = {
    "found": {
        "company_name": "Found",
        "campaigns": {
            "leads": {
                "monthly_budget": 1000,
                "goal_cm": 500,
                "goal_cac": 500,
                "rps": 2000,
                "variable_costs": 1000
            },
            "candidates": {
                "monthly_budget": 500,
            }
        }
    }
}
