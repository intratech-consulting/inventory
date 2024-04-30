



/* globals
*/

/* exported
    buildStatusDisplay,
    purchaseOrderStatusDisplay,
    returnOrderStatusDisplay,
    returnOrderLineItemStatusDisplay,
    salesOrderStatusDisplay,
    stockHistoryStatusDisplay,
    stockStatusDisplay,
*/


/*
 * Generic function to render a status label
 */
function renderStatusLabel(key, codes, options={}) {

    let text = null;
    let label = null;

    // Find the entry which matches the provided key
    for (var name in codes) {
        let entry = codes[name];

        if (entry.key == key) {
            text = entry.value;
            label = entry.label;
            break;
        }
    }

    if (!text) {
        console.error(`renderStatusLabel could not find match for code ${key}`);
    }

    // Fallback for color
    label = label || 'bg-dark';

    if (!text) {
        text = key;
    }

    let classes = `badge rounded-pill ${label}`;

    if (options.classes) {
        classes += ` ${options.classes}`;
    }

    return `<span class='${classes}'>${text}</span>`;
}



/*
 * Status codes for the stock model.
 * Generated from the values specified in "status_codes.py"
 */
const stockCodes = {
    
    'OK': {
        key: 10,
        value: 'OK',
        label: 'bg-success',
    },
    
    'ATTENTION': {
        key: 50,
        value: 'Vyžaduje pozornost',
        label: 'bg-warning',
    },
    
    'DAMAGED': {
        key: 55,
        value: 'Poškozeno',
        label: 'bg-warning',
    },
    
    'DESTROYED': {
        key: 60,
        value: 'Zničeno',
        label: 'bg-danger',
    },
    
    'REJECTED': {
        key: 65,
        value: 'Odmítnuto',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 70,
        value: 'Ztraceno',
        label: 'bg-dark',
    },
    
    'QUARANTINED': {
        key: 75,
        value: 'V karanténě',
        label: 'bg-info',
    },
    
    'RETURNED': {
        key: 85,
        value: 'Vráceno',
        label: 'bg-warning',
    },
    
};

/*
 * Render the status for a stock object.
 * Uses the values specified in "status_codes.py"
 */
function stockStatusDisplay(key, options={}) {
    return renderStatusLabel(key, stockCodes, options);
}



/*
 * Status codes for the stockHistory model.
 * Generated from the values specified in "status_codes.py"
 */
const stockHistoryCodes = {
    
    'LEGACY': {
        key: 0,
        value: 'Původní položka sledování zásob',
        label: 'bg-secondary',
    },
    
    'CREATED': {
        key: 1,
        value: 'Položka zásob vytvořena',
        label: 'bg-secondary',
    },
    
    'EDITED': {
        key: 5,
        value: 'Položka zásob upravena',
        label: 'bg-secondary',
    },
    
    'ASSIGNED_SERIAL': {
        key: 6,
        value: 'Přiřazeno výrobní číslo',
        label: 'bg-secondary',
    },
    
    'STOCK_COUNT': {
        key: 10,
        value: 'Stav zásob sečten',
        label: 'bg-secondary',
    },
    
    'STOCK_ADD': {
        key: 11,
        value: 'Zásoba přidána ručně',
        label: 'bg-secondary',
    },
    
    'STOCK_REMOVE': {
        key: 12,
        value: 'Zásoba odebrána ručně',
        label: 'bg-secondary',
    },
    
    'STOCK_MOVE': {
        key: 20,
        value: 'Umístění změněno',
        label: 'bg-secondary',
    },
    
    'STOCK_UPDATE': {
        key: 25,
        value: 'Stav zásob byl aktualizován',
        label: 'bg-secondary',
    },
    
    'INSTALLED_INTO_ASSEMBLY': {
        key: 30,
        value: 'Nainstalováno do sestavy',
        label: 'bg-secondary',
    },
    
    'REMOVED_FROM_ASSEMBLY': {
        key: 31,
        value: 'Odstraněno ze sestavy',
        label: 'bg-secondary',
    },
    
    'INSTALLED_CHILD_ITEM': {
        key: 35,
        value: 'Instalovaná položka komponenty',
        label: 'bg-secondary',
    },
    
    'REMOVED_CHILD_ITEM': {
        key: 36,
        value: 'Odstraněná komponenta',
        label: 'bg-secondary',
    },
    
    'SPLIT_FROM_PARENT': {
        key: 40,
        value: 'Rozdělit od nadřazené položky',
        label: 'bg-secondary',
    },
    
    'SPLIT_CHILD_ITEM': {
        key: 42,
        value: 'Rozdělit podřazený předmět',
        label: 'bg-secondary',
    },
    
    'MERGED_STOCK_ITEMS': {
        key: 45,
        value: 'Sloučené položky zásob',
        label: 'bg-secondary',
    },
    
    'CONVERTED_TO_VARIANT': {
        key: 48,
        value: 'Převedeno na variantu',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_CREATED': {
        key: 50,
        value: 'Výstup objednávky byl vytvořen',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_COMPLETED': {
        key: 55,
        value: 'Výstup objednávky sestavení dokončen',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_REJECTED': {
        key: 56,
        value: 'Výstup objednávky sestavení byl odmítnut',
        label: 'bg-secondary',
    },
    
    'BUILD_CONSUMED': {
        key: 57,
        value: 'Spotřebováno podle objednávky',
        label: 'bg-secondary',
    },
    
    'SHIPPED_AGAINST_SALES_ORDER': {
        key: 60,
        value: 'Odesláno v souladu se zákaznickou objednávkou',
        label: 'bg-secondary',
    },
    
    'RECEIVED_AGAINST_PURCHASE_ORDER': {
        key: 70,
        value: 'Přijato proti objednávce',
        label: 'bg-secondary',
    },
    
    'RETURNED_AGAINST_RETURN_ORDER': {
        key: 80,
        value: 'Vráceno proti vratce',
        label: 'bg-secondary',
    },
    
    'SENT_TO_CUSTOMER': {
        key: 100,
        value: 'Odesláno zákazníkovi',
        label: 'bg-secondary',
    },
    
    'RETURNED_FROM_CUSTOMER': {
        key: 105,
        value: 'Vráceno od zákazníka',
        label: 'bg-secondary',
    },
    
};

/*
 * Render the status for a stockHistory object.
 * Uses the values specified in "status_codes.py"
 */
function stockHistoryStatusDisplay(key, options={}) {
    return renderStatusLabel(key, stockHistoryCodes, options);
}



/*
 * Status codes for the build model.
 * Generated from the values specified in "status_codes.py"
 */
const buildCodes = {
    
    'PENDING': {
        key: 10,
        value: 'Nevyřízeno',
        label: 'bg-secondary',
    },
    
    'PRODUCTION': {
        key: 20,
        value: 'Výroba',
        label: 'bg-primary',
    },
    
    'CANCELLED': {
        key: 30,
        value: 'Zrušeno',
        label: 'bg-danger',
    },
    
    'COMPLETE': {
        key: 40,
        value: 'Hotovo',
        label: 'bg-success',
    },
    
};

/*
 * Render the status for a build object.
 * Uses the values specified in "status_codes.py"
 */
function buildStatusDisplay(key, options={}) {
    return renderStatusLabel(key, buildCodes, options);
}



/*
 * Status codes for the purchaseOrder model.
 * Generated from the values specified in "status_codes.py"
 */
const purchaseOrderCodes = {
    
    'PENDING': {
        key: 10,
        value: 'Nevyřízeno',
        label: 'bg-secondary',
    },
    
    'PLACED': {
        key: 20,
        value: 'Umístěno',
        label: 'bg-primary',
    },
    
    'COMPLETE': {
        key: 30,
        value: 'Hotovo',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'Zrušeno',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 50,
        value: 'Ztraceno',
        label: 'bg-warning',
    },
    
    'RETURNED': {
        key: 60,
        value: 'Vráceno',
        label: 'bg-warning',
    },
    
};

/*
 * Render the status for a purchaseOrder object.
 * Uses the values specified in "status_codes.py"
 */
function purchaseOrderStatusDisplay(key, options={}) {
    return renderStatusLabel(key, purchaseOrderCodes, options);
}



/*
 * Status codes for the salesOrder model.
 * Generated from the values specified in "status_codes.py"
 */
const salesOrderCodes = {
    
    'PENDING': {
        key: 10,
        value: 'Nevyřízeno',
        label: 'bg-secondary',
    },
    
    'IN_PROGRESS': {
        key: 15,
        value: 'Zpracovává se',
        label: 'bg-primary',
    },
    
    'SHIPPED': {
        key: 20,
        value: 'Odesláno',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'Zrušeno',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 50,
        value: 'Ztraceno',
        label: 'bg-warning',
    },
    
    'RETURNED': {
        key: 60,
        value: 'Vráceno',
        label: 'bg-warning',
    },
    
};

/*
 * Render the status for a salesOrder object.
 * Uses the values specified in "status_codes.py"
 */
function salesOrderStatusDisplay(key, options={}) {
    return renderStatusLabel(key, salesOrderCodes, options);
}



/*
 * Status codes for the returnOrder model.
 * Generated from the values specified in "status_codes.py"
 */
const returnOrderCodes = {
    
    'PENDING': {
        key: 10,
        value: 'Nevyřízeno',
        label: 'bg-secondary',
    },
    
    'IN_PROGRESS': {
        key: 20,
        value: 'Zpracovává se',
        label: 'bg-primary',
    },
    
    'COMPLETE': {
        key: 30,
        value: 'Hotovo',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'Zrušeno',
        label: 'bg-danger',
    },
    
};

/*
 * Render the status for a returnOrder object.
 * Uses the values specified in "status_codes.py"
 */
function returnOrderStatusDisplay(key, options={}) {
    return renderStatusLabel(key, returnOrderCodes, options);
}



/*
 * Status codes for the returnOrderLineItem model.
 * Generated from the values specified in "status_codes.py"
 */
const returnOrderLineItemCodes = {
    
    'PENDING': {
        key: 10,
        value: 'Nevyřízeno',
        label: 'bg-secondary',
    },
    
    'RETURN': {
        key: 20,
        value: 'Vrátit zpět',
        label: 'bg-success',
    },
    
    'REPAIR': {
        key: 30,
        value: 'Oprava',
        label: 'bg-primary',
    },
    
    'REPLACE': {
        key: 40,
        value: 'Náhrada',
        label: 'bg-warning',
    },
    
    'REFUND': {
        key: 50,
        value: 'Vrácení peněz',
        label: 'bg-info',
    },
    
    'REJECT': {
        key: 60,
        value: 'Odmítnout',
        label: 'bg-danger',
    },
    
};

/*
 * Render the status for a returnOrderLineItem object.
 * Uses the values specified in "status_codes.py"
 */
function returnOrderLineItemStatusDisplay(key, options={}) {
    return renderStatusLabel(key, returnOrderLineItemCodes, options);
}

