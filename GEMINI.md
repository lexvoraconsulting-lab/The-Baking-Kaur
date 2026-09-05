# AI Agent Instructions & Workspace Rules — The Baking Kaur

## 1. Framework Toolchain Architecture (ENV_FRM_01)
- **Central Framework Root:** All language runtimes, interpreters, and framework installations reside strictly in F:\frameworks\ (e.g. F:\frameworks\Python314).
- **Environment Mapping:** All execution commands and child processes must resolve Python and toolchains from F:\frameworks\Python314\python.exe and ensure system/user environment variables map to F:\frameworks\.
- **Zero Scattered Virtual Environments:** Do not create scattered virtual environments in the repository root or subfolders. All libraries (PyTorch, torchvision, transformers, requests, pytest) reside in the centralized framework environment.
- **Repository Scripts:** All .bat and automation scripts in 	ools-script/win/ must strictly target F:\frameworks\.

## 2. Storefront Protected Invariant (Rule 2.1)
- The product page (	emplates/product.json and sections/main-product-premium-v2.liquid) is strictly locked against any visual, UX, purchase-flow, CSS, or JS changes.

## 3. Deployment Protocol (Rule 5.2)
- Always preview and test theme work on development theme or preview theme (#152070258857) on e86ba-2a.myshopify.com. Never push directly to live without differential authorization.
