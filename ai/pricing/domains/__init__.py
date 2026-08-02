"""
Enterprise Pricing Intelligence Engine - domain extension points.

WHY THIS PACKAGE EXISTS, SEPARATE FROM ai.pricing's TOP LEVEL
  ai.pricing (models/repository/strategy/service/audit) is the AI-token
  usage engine - complete, tested, live-wired into ai/vision today. This
  package generalizes the same Repository+Strategy shape to other pricing
  domains a cake business actually has (delivery, discounts, corporate
  rates, ...) without merging them into one undifferentiated module.

WHY SOME DOMAINS HAVE A REAL STRATEGY AND OTHERS ARE INTERFACE-ONLY
  discounts_promotions.py, corporate_pricing.py, and delivery.py implement
  real, generic, tested math (a percentage discount, a volume tier, a
  distance band) that requires no business-specific facts to be correct -
  the caller supplies the actual numbers. recipe_costing.py, packaging.py,
  customization.py, erp_integration.py, and ai_quote_generation.py are
  interface-only: this project's own standing rule is "never invent" (no
  fabricated GTINs, ratings, or delivery promises elsewhere in this repo),
  and real ingredient costs, packaging rates, an actual ERP system, and a
  quote-generation spec are exactly that kind of fact nobody has supplied.
  Each interface-only module states in its own docstring what real input is
  needed before a concrete implementation can be written - the extension
  point exists so that's a config/data problem when it happens, not a
  redesign.

WHY THESE ARE OPT-IN IMPORTS, NOT RE-EXPORTED FROM ai.pricing's __init__
  ai.pricing.__init__ is the AI-usage engine's stable public surface,
  already used by ai/vision. Nine more names in that same namespace with no
  live caller yet would be exactly the "folder with no second tenant"
  ai/vision/python's own FolderStructure.md warns against - import each
  domain from its own submodule (ai.pricing.domains.delivery import ...).
"""
