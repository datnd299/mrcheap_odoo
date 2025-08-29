{
    "name": "MrCheap",
    "version": "18.0.2.0.0",
    "summary": "Simple sample app for inexpensive items",
    "description": "Quản lý danh sách sản phẩm giá rẻ (demo).",
    "author": "Dat Nguyen",
    "website": "https://example.com",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base", "account"],  # cần tối thiểu 'base'
    "data": [
        "security/ir.model.access.csv",
        "views/mrcheap_menu.xml",
        "views/mrcheap_views.xml",
        "views/res_partner_view.xml"
    ],
    "application": True,   # để hiện trong Apps menu
}