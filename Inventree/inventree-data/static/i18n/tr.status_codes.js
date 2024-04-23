



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
        value: 'TAMAM',
        label: 'bg-success',
    },
    
    'ATTENTION': {
        key: 50,
        value: 'Dikkat gerekli',
        label: 'bg-warning',
    },
    
    'DAMAGED': {
        key: 55,
        value: 'Hasarlı',
        label: 'bg-warning',
    },
    
    'DESTROYED': {
        key: 60,
        value: 'Kullanılamaz durumda',
        label: 'bg-danger',
    },
    
    'REJECTED': {
        key: 65,
        value: 'Reddedildi',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 70,
        value: 'Kayıp',
        label: 'bg-dark',
    },
    
    'QUARANTINED': {
        key: 75,
        value: 'Karantinaya alındı',
        label: 'bg-info',
    },
    
    'RETURNED': {
        key: 85,
        value: 'İade',
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
        value: 'Eski stok izleme girişi',
        label: 'bg-secondary',
    },
    
    'CREATED': {
        key: 1,
        value: 'Stok kalemi oluşturuldu',
        label: 'bg-secondary',
    },
    
    'EDITED': {
        key: 5,
        value: 'Düzenlenen stok kalemi',
        label: 'bg-secondary',
    },
    
    'ASSIGNED_SERIAL': {
        key: 6,
        value: 'Atanan seri numarası',
        label: 'bg-secondary',
    },
    
    'STOCK_COUNT': {
        key: 10,
        value: 'Stok sayıldı',
        label: 'bg-secondary',
    },
    
    'STOCK_ADD': {
        key: 11,
        value: 'Stok manuel olarak eklendi',
        label: 'bg-secondary',
    },
    
    'STOCK_REMOVE': {
        key: 12,
        value: 'Stok manuel olarak çıkarıldı',
        label: 'bg-secondary',
    },
    
    'STOCK_MOVE': {
        key: 20,
        value: 'Konum değişti',
        label: 'bg-secondary',
    },
    
    'STOCK_UPDATE': {
        key: 25,
        value: 'Stok Güncellendi',
        label: 'bg-secondary',
    },
    
    'INSTALLED_INTO_ASSEMBLY': {
        key: 30,
        value: 'Montajda kullanıldı',
        label: 'bg-secondary',
    },
    
    'REMOVED_FROM_ASSEMBLY': {
        key: 31,
        value: 'Montajdan çıkarıldı',
        label: 'bg-secondary',
    },
    
    'INSTALLED_CHILD_ITEM': {
        key: 35,
        value: 'Bileşen ögesinde kullanıldı',
        label: 'bg-secondary',
    },
    
    'REMOVED_CHILD_ITEM': {
        key: 36,
        value: 'Bileşen ögesinden çıkarıldı',
        label: 'bg-secondary',
    },
    
    'SPLIT_FROM_PARENT': {
        key: 40,
        value: 'Üst ögeden ayır',
        label: 'bg-secondary',
    },
    
    'SPLIT_CHILD_ITEM': {
        key: 42,
        value: 'Alt ögeyi ayır',
        label: 'bg-secondary',
    },
    
    'MERGED_STOCK_ITEMS': {
        key: 45,
        value: 'Stok parçalarını birleştir',
        label: 'bg-secondary',
    },
    
    'CONVERTED_TO_VARIANT': {
        key: 48,
        value: 'Converted to variant',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_CREATED': {
        key: 50,
        value: 'Yapım emri çıktısı oluşturuldu',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_COMPLETED': {
        key: 55,
        value: 'Yapım emri çıktısı tamamlandı',
        label: 'bg-secondary',
    },
    
    'BUILD_OUTPUT_REJECTED': {
        key: 56,
        value: 'Build order output rejected',
        label: 'bg-secondary',
    },
    
    'BUILD_CONSUMED': {
        key: 57,
        value: 'Consumed by build order',
        label: 'bg-secondary',
    },
    
    'SHIPPED_AGAINST_SALES_ORDER': {
        key: 60,
        value: 'Shipped against Sales Order',
        label: 'bg-secondary',
    },
    
    'RECEIVED_AGAINST_PURCHASE_ORDER': {
        key: 70,
        value: 'Received against Purchase Order',
        label: 'bg-secondary',
    },
    
    'RETURNED_AGAINST_RETURN_ORDER': {
        key: 80,
        value: 'Returned against Return Order',
        label: 'bg-secondary',
    },
    
    'SENT_TO_CUSTOMER': {
        key: 100,
        value: 'Müşteriye gönderildi',
        label: 'bg-secondary',
    },
    
    'RETURNED_FROM_CUSTOMER': {
        key: 105,
        value: 'Müşteriden geri döndü',
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
        value: 'Bekliyor',
        label: 'bg-secondary',
    },
    
    'PRODUCTION': {
        key: 20,
        value: 'Üretim',
        label: 'bg-primary',
    },
    
    'CANCELLED': {
        key: 30,
        value: 'İptal edildi',
        label: 'bg-danger',
    },
    
    'COMPLETE': {
        key: 40,
        value: 'Tamamlandı',
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
        value: 'Bekliyor',
        label: 'bg-secondary',
    },
    
    'PLACED': {
        key: 20,
        value: 'Sipariş verildi',
        label: 'bg-primary',
    },
    
    'COMPLETE': {
        key: 30,
        value: 'Tamamlandı',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'İptal edildi',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 50,
        value: 'Kayıp',
        label: 'bg-warning',
    },
    
    'RETURNED': {
        key: 60,
        value: 'İade',
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
        value: 'Bekliyor',
        label: 'bg-secondary',
    },
    
    'IN_PROGRESS': {
        key: 15,
        value: 'Devam Ediyor',
        label: 'bg-primary',
    },
    
    'SHIPPED': {
        key: 20,
        value: 'Sevk edildi',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'İptal edildi',
        label: 'bg-danger',
    },
    
    'LOST': {
        key: 50,
        value: 'Kayıp',
        label: 'bg-warning',
    },
    
    'RETURNED': {
        key: 60,
        value: 'İade',
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
        value: 'Bekliyor',
        label: 'bg-secondary',
    },
    
    'IN_PROGRESS': {
        key: 20,
        value: 'Devam Ediyor',
        label: 'bg-primary',
    },
    
    'COMPLETE': {
        key: 30,
        value: 'Tamamlandı',
        label: 'bg-success',
    },
    
    'CANCELLED': {
        key: 40,
        value: 'İptal edildi',
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
        value: 'Bekliyor',
        label: 'bg-secondary',
    },
    
    'RETURN': {
        key: 20,
        value: 'Geri Dön',
        label: 'bg-success',
    },
    
    'REPAIR': {
        key: 30,
        value: 'Repair',
        label: 'bg-primary',
    },
    
    'REPLACE': {
        key: 40,
        value: 'Replace',
        label: 'bg-warning',
    },
    
    'REFUND': {
        key: 50,
        value: 'Refund',
        label: 'bg-info',
    },
    
    'REJECT': {
        key: 60,
        value: 'Reject',
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

