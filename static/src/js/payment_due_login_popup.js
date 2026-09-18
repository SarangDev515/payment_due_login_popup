/** @odoo-module **/

import { Component, reactive } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
import { session } from "@web/session";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";


export class PaymentDueDialog extends Component {
      static template = "payment_due_login_popup.PaymentDueDialog";
      static components = { Dialog };
      static props = {
                close: Function,
                data: Object,
                onMinimize: Function,
                title: String,
      };

    setup() {
              this.action = useService("action");
    }

    minimize() {
              this.props.onMinimize();
    }

    openMove(item) {
              // Keep the reminder available while the user reviews the document.
          // This is especially useful when several due records are listed.
          this.props.onMinimize();
              this.action.doAction({
                            type: "ir.actions.act_window",
                            res_model: "account.move",
                            res_id: item.id,
                            views: [[false, "form"]],
                            context: {
                                              create: false,
                            },
              });
    }
}


export class PaymentDueMinibox extends Component {
      static template = "payment_due_login_popup.PaymentDueMinibox";
      static props = {
                close: Function,
                restore: Function,
                state: Object,
      };

}


export const paymentDueLoginPopupService = {
      dependencies: ["orm", "dialog"],

      start(env, { orm, dialog }) {
                const storageKey = `payment_due_login_popup.dismissed.${session.db || "default"}.${session.uid || "guest"}`;
                let hasCheckedThisSession = browser.sessionStorage.getItem(storageKey) === "1";
                let removeDialog = null;
                let minimizing = false;
                const state = reactive({
                              data: null,
                              minimized: false,
                });

          const markDismissed = () => {
                        hasCheckedThisSession = true;
                        browser.sessionStorage.setItem(storageKey, "1");
          };

          const clearDismissed = () => {
                        hasCheckedThisSession = false;
                        browser.sessionStorage.removeItem(storageKey);
          };

          const closeMinibox = () => {
                        markDismissed();
                        state.minimized = false;
                        state.data = null;
          };

          const handleLogoutClick = (event) => {
                        const link = event.target instanceof Element ? event.target.closest("a[href*='/web/session/logout']") : null;
                        if (link) {
                                          clearDismissed();
                        }
          };

          browser.addEventListener("click", handleLogoutClick, true);

          const openDialog = (data) => {
                        if (removeDialog) {
                                          return;
                        }
                        state.data = data;
                        state.minimized = false;
                        minimizing = false;
                        removeDialog = dialog.add(
                                          PaymentDueDialog,
                          {
                                                data,
                                                onMinimize: () => {
                                                                          if (!removeDialog || minimizing) {
                                                                                                        return;
                                                                            }
                                                                          minimizing = true;
                                                                          removeDialog();
                                                },
                                                title: _t("Payments Due"),
                          },
                          {
                                                onClose: () => {
                                                                          const wasMinimized = minimizing;
                                                                          removeDialog = null;
                                                                          minimizing = false;
                                                                          if (wasMinimized) {
                                                                                                        state.minimized = true;
                                                                            } else {
                                                                                                        markDismissed();
                                                                                                        state.minimized = false;
                                                                                                        state.data = null;
                                                                            }
                                                },
                          }
                                      );
          };

          const restoreDialog = () => {
                        if (state.data && !removeDialog) {
                                          openDialog(state.data);
                        }
          };

          registry.category("main_components").add(
                        "payment_due_login_popup.Minibox",
            {
                              Component: PaymentDueMinibox,
                              props: {
                                                    close: closeMinibox,
                                                    restore: restoreDialog,
                                                    state,
                              },
            }
                    );

          const checkForDuePayments = async () => {
                        if (hasCheckedThisSession) {
                                          return;
                        }
                        hasCheckedThisSession = true;

                        let data;
                        try {
                                          // Use the silent ORM wrapper because users without accounting
                            // access should simply not receive the reminder dialog.
                            data = await orm.silent.call(
                                                  "account.move",
                                                  "get_due_payment_popup_data"
                                              );
                        } catch {
                                          return;
                        }

                        if (data?.total_count) {
                                          openDialog(data);
                        }
          };

          // Do not add an overlay before the main web client has mounted.
          env.bus.addEventListener("WEB_CLIENT_READY", checkForDuePayments, { once: true });

          return {
                        checkForDuePayments,
                        closeMinibox,
                        restoreDialog,
          };
      },
};

registry.category("services").add(
      "paymentDueLoginPopup",
      paymentDueLoginPopupService
  );
