/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

registry.category("actions").add("mrcheap_copy_link", async (env, action) => {
    const url = action && action.params && action.params.url;
    if (!url) {
        env.services.notification.add(_t("Payment link is empty."), { type: "warning" });
        return;
    }
    try {
        await navigator.clipboard.writeText(url);
        env.services.notification.add(_t("Copied payment link."), { type: "success" });
    } catch (e) {
        // Fallback
        const ta = document.createElement("textarea");
        ta.value = url;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch {}
        document.body.removeChild(ta);
        env.services.notification.add(_t("Copied payment link."), { type: "success" });
    }
    return; // hoàn tất action
});
