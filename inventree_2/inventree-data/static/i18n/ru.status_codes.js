



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
        value: 'Да',
        label: 'bg-success',
    },
    
    'ATTENTION': {
        key: 50,
        value: 'Требует внимания',
        label: 'bg-warning',
    },
    
    'DAMAGED': {
        key: 55,
        value: 'Поврежденный',
        label: 'bg-warning',
    },
    
    'DESTROYED': {
        key: 60,
        value: 'Разрушено',
        label: 'bg-danger',
    },
    
    'REJECTED': {
        key: 65,
        value: 'Отклоненный',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 70,
        value: 'Потерян',
        label: 'bg-dark',
    },
    
    'QUARANTINED': {
        key: 75,
        value: 'Карантин',
        label: 'bg-info',
    },
    
    'RETURNED': {
        key: 85,
        value: 'Возвращено',
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
        value: 'Отслеживание устаревших запасов',
        label: 'bg-secondary',
    },
    
    'CREATED': {
        key: 1,
        value: 'Складская позиция создана',
        label: 'bg-secondary',
    },
    
    'EDITED': {
        key: 5,
        value: 'Отредактированная складская позиция',
        label: 'bg-secondary',
    },
    
    'ASSIGNED_SERIAL': {
        key: 6,
        value: 'Присвоенный серийный номер',
        label: 'bg-secondary',
    },
    
    'STOCK_COUNT': {
        key: 10,
        value: 'Новое значение запасов установлено',
        label: 'bg-secondary',
    },
    
    'STOCK_ADD': {
        key: 11,
        value: 'Запасы, добавленные вручную',
        label: 'bg-secondary',
    },
    
    'STOCK_REMOVE': {
        key: 12,
        value: 'Запасы удаленные вручную',
        label: 'bg-secondary',
    },
    
    'STOCK_MOVE': {
        key: 20,
        value: 'Место хранения изменено',
        label: 'bg-secondary',
    },
    
    'STOCK_UPDATE': {
        key: 25,
        value: 'Запас обновлен',
        label: 'bg-secondary',
    },
    
    'INSTALLED_INTO_ASSEMBLY': {
        key: 30,
        value: 'Установленно в производимую деталь',
        label: 'bg-secondary',
    },
    
    'REMOVED_FROM_ASSEMBLY': {
        key: 31,
        value: 'Удалено из производимой детали',
        label: 'bg-secondary',
    },
    
    'INSTALLED_CHILD_ITEM': {
        key: 35,
        value: 'Установленный компонент',
        label: 'bg-secondary',
    },
    
    'REMOVED_CHILD_ITEM': {
        key: 36,
        value: 'Удаленный компонент',
        label: 'bg-secondary',
    },
    
    'SPLIT_FROM_PARENT': {
        key: 40,
        value: 'Отделить от родительского элемента',
        label: 'bg-secondary',
    },
    
    'SPLIT_CHILD_ITEM': {
        key: 42,
        value: 'Разбить дочерний элемент',
        label: 'bg-secondary',
    },
    
    'MERGED_STOCK_ITEMS': {
        key: 45,
        value: 'Объединенные складские позиции',
        label: 'bg-secondary',
    },
    
    'CONVERTED_TO_VARIANT': {
        key: 48,
        value: 'Преобразовать в разновидность',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_CREATED': {
        key: 50,
        value: 'Создан выход продукции для этого заказа на производство',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_COMPLETED': {
        key: 55,
        value: 'Продукция заказа на производство завершена',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_REJECTED': {
        key: 56,
        value: 'Продукция заказа на производство отклонена',
        label: 'bg-secondary',
    },
    
    'BUILD_CONSUMED': {
        key: 57,
        value: 'Поглощен заказом на производство',
        label: 'bg-secondary',
    },
    
    'SHIPPED_AGAINST_SALES_ORDER': {
        key: 60,
        value: 'Отгружено по заказу на продажу',
        label: 'bg-secondary',
    },
    
    'RECEIVED_AGAINST_PURCHASE_ORDER': {
        key: 70,
        value: 'Получено по заказу на поставку',
        label: 'bg-secondary',
    },
    
    'RETURNED_AGAINST_RETURN_ORDER': {
        key: 80,
        value: 'Возвращено по заказу на возврат',
        label: 'bg-secondary',
    },
    
    'SENT_TO_CUSTOMER': {
        key: 100,
        value: 'Отправлено клиенту',
        label: 'bg-secondary',
    },
    
    'RETURNED_FROM_CUSTOMER': {
        key: 105,
        value: 'Возвращено от клиента',
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
        value: 'Ожидаемый',
        label: 'bg-secondary',
    },
    
    'PRODUCTION': {
        key: 20,
        value: 'Продукция',
        label: 'bg-primary',
    },
    
    'CANCELLED': {
        key: 30,
        value: 'Отменено',
        label: 'bg-danger',
    },
    
    'COMPLETE': {
        key: 40,
        value: 'Готово',
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
        value: 'Ожидаемый',
        label: 'bg-secondary',
    },
    
    'PLACED': {
        key: 20,
        value: 'Размещены',
        label: 'bg-primary',
    },
    
    'COMPLETE': {
        key: 30,
        value: 'Готово',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'Отменено',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 50,
        value: 'Потерян',
        label: 'bg-warning',
    },
    
    'RETURNED': {
        key: 60,
        value: 'Возвращено',
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
        value: 'Ожидаемый',
        label: 'bg-secondary',
    },
    
    'IN_PROGRESS': {
        key: 15,
        value: 'Выполняется',
        label: 'bg-primary',
    },
    
    'SHIPPED': {
        key: 20,
        value: 'Доставлено',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'Отменено',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 50,
        value: 'Потерян',
        label: 'bg-warning',
    },
    
    'RETURNED': {
        key: 60,
        value: 'Возвращено',
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
        value: 'Ожидаемый',
        label: 'bg-secondary',
    },
    
    'IN_PROGRESS': {
        key: 20,
        value: 'Выполняется',
        label: 'bg-primary',
    },
    
    'COMPLETE': {
        key: 30,
        value: 'Готово',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'Отменено',
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
        value: 'Ожидаемый',
        label: 'bg-secondary',
    },
    
    'RETURN': {
        key: 20,
        value: 'Возврат',
        label: 'bg-success',
    },
    
    'REPAIR': {
        key: 30,
        value: 'Починить',
        label: 'bg-primary',
    },
    
    'REPLACE': {
        key: 40,
        value: 'Заменить',
        label: 'bg-warning',
    },
    
    'REFUND': {
        key: 50,
        value: 'Возврат',
        label: 'bg-info',
    },
    
    'REJECT': {
        key: 60,
        value: 'Отклонить',
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

