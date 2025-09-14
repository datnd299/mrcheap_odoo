{
    "name": "MrCheap",
    "version": "18.0.2.0.1",
    "summary": "Simple sample app for inexpensive items",
    "description": "Quản lý danh sách sản phẩm giá rẻ (demo).",
    "author": "Dat Nguyen",
    "website": "https://example.com",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base", "account", "sale", "website", "payment"],  # cần tối thiểu 'base'
    "data": [
        "security/ir.model.access.csv",
        "views/mrcheap_menu.xml",
        "views/mrcheap_views.xml",
        "views/res_partner_view.xml",
        "views/payment_transfer_vietqr.xml",
        "views/account_move_view.xml",
        "views/account_journal_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "mrcheap/static/src/js/payment_poll.js",
        ],
        "web.assets_backend": [
            "mrcheap/static/src/js/copy_payment_link_action.js",
        ],
    },
    "application": True,   # để hiện trong Apps menu
}