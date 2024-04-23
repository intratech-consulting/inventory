import{r as i,i as t,j as s,a3 as I,b7 as g,ay as v,b8 as N,b9 as O,ba as G,b6 as L,bb as U,bc as W,bd as B,aw as Y,be as Q,bf as K,bg as V,bh as z,S as q,m as H}from"./vendor-580d7f6a.js";import{I as J,D as F}from"./ItemDetails-8f9834aa.js";import{D as Z,N as X}from"./MarkdownEditor-8fcb1f1c.js";import{A as $,E as ee,D as se}from"./ActionDropdown-0b7f88be.js";import{P as te}from"./PageDetail-e83b8dc6.js";import{P as ae}from"./PanelGroup-ecf19d17.js";import{a as C,A as l,U as o,i as A}from"./index-539d0685.js";import{c as re}from"./CompanyForms-f616143f.js";import{a as S,u as w,b as T}from"./UseForm-5e9a21d6.js";import{u as oe}from"./UseInstance-05463349.js";import{A as D}from"./AddItemButton-9bde5586.js";import{Y as ie}from"./YesNoButton-cd4c504e.js";import{u as M,R as P,a as E,I as y}from"./InvenTreeTable-7dffc519.js";import{A as le}from"./AttachmentTable-3bae0b2b.js";import{M as ne}from"./ManufacturerPartTable-4fd3748c.js";import{P as ce}from"./PurchaseOrderTable-e32429c5.js";import{S as de}from"./SupplierPartTable-5f41232e.js";import{R as pe}from"./ReturnOrderTable-bdcacb6a.js";import{S as ue}from"./SalesOrderTable-f3e08017.js";import{S as R}from"./StockItemTable-b84d5ecc.js";import{a as me}from"./DesktopAppView-f36ad07f.js";import"./urls-9eea01e5.js";import"./ModelType-07300e1e.js";import"./ProgressBar-f667695e.js";import"./Instance-4f17d9b0.js";import"./BaseContext-71d55e61.js";import"./StylishText-5ee5b946.js";import"./notifications-b554622d.js";import"./Placeholder-f60056df.js";import"./ApiForm-173d0ec5.js";import"./ColumnRenderers-c7f5177c.js";import"./PurchaseOrderForms-075e7f87.js";import"./StockForms-2847fb41.js";function be({companyId:d,params:p}){const a=C(),e=M("address"),f=i.useMemo(()=>[{accessor:"title",sortable:!0,switchable:!1},{accessor:"primary",switchable:!1,sortable:!1,render:r=>ie({value:r.primary})},{accessor:"address",title:t._({id:"Du6bPw"}),sortable:!1,switchable:!1,render:r=>{let _="";return r!=null&&r.line1&&(_+=r.line1),r!=null&&r.line2&&(_+=" "+r.line2),_.trim()}},{accessor:"postal_code",sortable:!1,switchable:!0},{accessor:"postal_city",sortable:!1,switchable:!0},{accessor:"province",sortable:!1,switchable:!0},{accessor:"country",sortable:!1,switchable:!0},{accessor:"shipping_notes",sortable:!1,switchable:!0},{accessor:"internal_shipping_notes",sortable:!1,switchable:!0},{accessor:"link",sortable:!1,switchable:!0}],[]),n=i.useMemo(()=>({company:{},title:{},primary:{},line1:{},line2:{},postal_code:{},postal_city:{},province:{},country:{},shipping_notes:{},internal_shipping_notes:{},link:{}}),[]),u=S({url:l.address_list,title:t._({id:"W0pjLr"}),fields:n,initialData:{company:d},successMessage:t._({id:"N0ZOat"}),onFormSuccess:e.refreshTable}),[m,c]=i.useState(-1),b=w({url:l.address_list,pk:m,title:t._({id:"xLQ0lF"}),fields:n,onFormSuccess:e.refreshTable}),h=T({url:l.address_list,pk:m,title:t._({id:"xiRN5x"}),onFormSuccess:e.refreshTable,preFormWarning:t._({id:"F1bgq9"})}),x=i.useCallback(r=>{let _=a.hasChangeRole(o.purchase_order)||a.hasChangeRole(o.sales_order),j=a.hasDeleteRole(o.purchase_order)||a.hasDeleteRole(o.sales_order);return[P({hidden:!_,onClick:()=>{c(r.pk),b.open()}}),E({hidden:!j,onClick:()=>{c(r.pk),h.open()}})]},[a]),k=i.useMemo(()=>{let r=a.hasChangeRole(o.purchase_order)||a.hasChangeRole(o.sales_order);return[s.jsx(D,{tooltip:t._({id:"W0pjLr"}),onClick:()=>u.open(),disabled:!r})]},[a]);return s.jsxs(s.Fragment,{children:[u.modal,b.modal,h.modal,s.jsx(y,{url:A(l.address_list),tableState:e,columns:f,props:{rowActions:x,tableActions:k,params:{...p,company:d}}})]})}function he({companyId:d,params:p}){const a=C(),e=M("contact"),f=i.useMemo(()=>[{accessor:"name",sortable:!0,switchable:!1},{accessor:"phone",switchable:!0,sortable:!1},{accessor:"email",switchable:!0,sortable:!1},{accessor:"role",switchable:!0,sortable:!1}],[]),n=i.useMemo(()=>({company:{},name:{},phone:{},email:{},role:{}}),[]),[u,m]=i.useState(void 0),c=w({url:l.contact_list,pk:u,title:t._({id:"mQpWAe"}),fields:n,onFormSuccess:e.refreshTable}),b=S({url:l.contact_list,title:t._({id:"M0FgOk"}),initialData:{company:d},fields:n,onFormSuccess:e.refreshTable}),h=T({url:l.contact_list,pk:u,title:t._({id:"0oMKRL"}),onFormSuccess:e.refreshTable}),x=i.useCallback(r=>{let _=a.hasChangeRole(o.purchase_order)||a.hasChangeRole(o.sales_order),j=a.hasDeleteRole(o.purchase_order)||a.hasDeleteRole(o.sales_order);return[P({hidden:!_,onClick:()=>{m(r.pk),c.open()}}),E({hidden:!j,onClick:()=>{m(r.pk),h.open()}})]},[a]),k=i.useMemo(()=>{let r=a.hasAddRole(o.purchase_order)||a.hasAddRole(o.sales_order);return[s.jsx(D,{tooltip:t._({id:"QsNWTM"}),onClick:()=>b.open(),disabled:!r})]},[a]);return s.jsxs(s.Fragment,{children:[b.modal,c.modal,h.modal,s.jsx(y,{url:A(l.contact_list),tableState:e,columns:f,props:{rowActions:x,tableActions:k,params:{...p,company:d}}})]})}function He(d){const{id:p}=me(),a=C(),{instance:e,refreshInstance:f,instanceQuery:n}=oe({endpoint:l.company_list,pk:p,params:{},refetchOnMount:!0}),u=i.useMemo(()=>{if(n.isFetching)return s.jsx(I,{});let h=[{type:"text",name:"description",label:t._({id:"Nu4oKW"})},{type:"link",name:"website",label:t._({id:"On0aF2"}),external:!0,copy:!0,hidden:!e.website},{type:"text",name:"phone",label:t._({id:"HF6C2L"}),copy:!0,hidden:!e.phone},{type:"text",name:"email",label:t._({id:"hzKQCy"}),copy:!0,hidden:!e.email}],x=[{type:"string",name:"currency",label:t._({id:"xjO9oI"})},{type:"boolean",name:"is_supplier",label:t._({id:"PYTEl0"}),icon:"suppliers"},{type:"boolean",name:"is_manufacturer",label:t._({id:"+m9/3S"}),icon:"manufacturers"},{type:"boolean",name:"is_customer",label:t._({id:"876pfE"}),icon:"customers"}];return s.jsxs(J,{children:[s.jsxs(g,{children:[s.jsx(g.Col,{span:4,children:s.jsx(Z,{appRole:o.purchase_order,apiPath:l.company_list,src:e.image,pk:e.pk,refresh:f,imageActions:{uploadFile:!0,deleteFile:!0}})}),s.jsx(g.Col,{span:8,children:s.jsx(F,{item:e,fields:h})})]}),s.jsx(F,{item:e,fields:x})]})},[e,n]),m=i.useMemo(()=>[{name:"details",label:t._({id:"URmyfc"}),icon:s.jsx(v,{}),content:u},{name:"manufactured-parts",label:t._({id:"glJbgw"}),icon:s.jsx(N,{}),hidden:!(e!=null&&e.is_manufacturer),content:(e==null?void 0:e.pk)&&s.jsx(ne,{params:{manufacturer:e.pk}})},{name:"supplied-parts",label:t._({id:"i4b9ex"}),icon:s.jsx(O,{}),hidden:!(e!=null&&e.is_supplier),content:(e==null?void 0:e.pk)&&s.jsx(de,{params:{supplier:e.pk}})},{name:"purchase-orders",label:t._({id:"85Yvr2"}),icon:s.jsx(G,{}),hidden:!(e!=null&&e.is_supplier),content:(e==null?void 0:e.pk)&&s.jsx(ce,{supplierId:e.pk})},{name:"stock-items",label:t._({id:"Jbck4N"}),icon:s.jsx(L,{}),hidden:!(e!=null&&e.is_manufacturer)&&!(e!=null&&e.is_supplier),content:(e==null?void 0:e.pk)&&s.jsx(R,{params:{company:e.pk}})},{name:"sales-orders",label:t._({id:"B1TL+X"}),icon:s.jsx(U,{}),hidden:!(e!=null&&e.is_customer),content:(e==null?void 0:e.pk)&&s.jsx(ue,{customerId:e.pk})},{name:"return-orders",label:t._({id:"LlTg8M"}),icon:s.jsx(W,{}),hidden:!(e!=null&&e.is_customer),content:e.pk&&s.jsx(pe,{params:{customer:e.pk}})},{name:"assigned-stock",label:t._({id:"TVGEcl"}),icon:s.jsx(B,{}),hidden:!(e!=null&&e.is_customer),content:e!=null&&e.pk?s.jsx(R,{params:{customer:e.pk}}):s.jsx(I,{})},{name:"contacts",label:t._({id:"gVfVfe"}),icon:s.jsx(Y,{}),content:(e==null?void 0:e.pk)&&s.jsx(he,{companyId:e.pk})},{name:"addresses",label:t._({id:"bYmAV1"}),icon:s.jsx(Q,{}),content:(e==null?void 0:e.pk)&&s.jsx(be,{companyId:e.pk})},{name:"attachments",label:t._({id:"w/Sphq"}),icon:s.jsx(K,{}),content:s.jsx(le,{endpoint:l.company_attachment_list,model:"company",pk:e.pk??-1})},{name:"notes",label:t._({id:"1DBGsz"}),icon:s.jsx(V,{}),content:s.jsx(X,{url:A(l.company_list,e.pk),data:(e==null?void 0:e.notes)??"",allowEdit:!0})}],[p,e]),c=w({url:l.company_list,pk:e==null?void 0:e.pk,title:t._({id:"HoG6cl"}),fields:re(),onFormSuccess:f}),b=i.useMemo(()=>[s.jsx($,{tooltip:t._({id:"z+ZEYC"}),icon:s.jsx(z,{}),actions:[ee({disabled:!a.hasChangeRole(o.purchase_order),onClick:()=>c.open()}),se({disabled:!a.hasDeleteRole(o.purchase_order)})]},"company")],[p,e,a]);return s.jsxs(s.Fragment,{children:[c.modal,s.jsxs(q,{spacing:"xs",children:[s.jsx(H,{visible:n.isFetching}),s.jsx(te,{title:t._({id:"7i8j3G"})+`: ${e.name}`,subtitle:e.description,actions:b,imageUrl:e.image,breadcrumbs:d.breadcrumbs}),s.jsx(ae,{pageKey:"company",panels:m})]})]})}export{He as default};
