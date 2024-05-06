import{r as d,j as e,a3 as c,i as s,b7 as l,ay as h,bt as f,d6 as g,bb as k,bn as I,bf as P,bg as C,S as D,m as F}from"./vendor-580d7f6a.js";import{I as A,D as i}from"./ItemDetails-8f9834aa.js";import{D as T,N as U}from"./MarkdownEditor-8fcb1f1c.js";import{P as E}from"./PageDetail-e83b8dc6.js";import{P as S}from"./PanelGroup-ecf19d17.js";import{A as r,M as n,U as N,i as v}from"./index-539d0685.js";import{u as B}from"./UseInstance-05463349.js";import{B as Q}from"./BuildOrderTable-0f548787.js";import{A as q}from"./AttachmentTable-3bae0b2b.js";import{a as G}from"./DesktopAppView-f36ad07f.js";import"./urls-9eea01e5.js";import"./ModelType-07300e1e.js";import"./ProgressBar-f667695e.js";import"./YesNoButton-cd4c504e.js";import"./Instance-4f17d9b0.js";import"./BaseContext-71d55e61.js";import"./InvenTreeTable-7dffc519.js";import"./notifications-b554622d.js";import"./ApiForm-173d0ec5.js";import"./StylishText-5ee5b946.js";import"./Placeholder-f60056df.js";import"./AddItemButton-9bde5586.js";import"./ColumnRenderers-c7f5177c.js";import"./UseForm-5e9a21d6.js";function me(){var m;const{id:a}=G(),{instance:t,instanceQuery:o}=B({endpoint:r.sales_order_list,pk:a,params:{customer_detail:!0}}),u=d.useMemo(()=>{var p;if(o.isFetching)return e.jsx(c,{});let b=[{type:"text",name:"reference",label:s._({id:"N2C89m"}),copy:!0},{type:"text",name:"customer_reference",label:s._({id:"ZVUe1A"}),copy:!0,hidden:!t.customer_reference},{type:"link",name:"customer",icon:"customers",label:s._({id:"876pfE"}),model:n.company},{type:"text",name:"description",label:s._({id:"Nu4oKW"}),copy:!0},{type:"status",name:"status",label:s._({id:"uAQUqI"}),model:n.salesorder}],x=[{type:"text",name:"line_items",label:s._({id:"SgduFH"}),icon:"list"},{type:"progressbar",name:"completed",icon:"progress",label:s._({id:"qgs95u"}),total:t.line_items,progress:t.completed_lines},{type:"progressbar",name:"shipments",icon:"shipment",label:s._({id:"polrQd"}),total:t.shipments,progress:t.completed_shipments},{type:"text",name:"currency",label:s._({id:"9j2hXW"})},{type:"text",name:"total_cost",label:s._({id:"A6C0pv"})}],j=[{type:"link",external:!0,name:"link",label:s._({id:"yzF66j"}),copy:!0,hidden:!t.link},{type:"link",model:n.contact,link:!1,name:"contact",label:s._({id:"jfC/xh"}),icon:"user",copy:!0}],y=[{type:"text",name:"creation_date",label:s._({id:"x9P/+F"}),icon:"calendar"},{type:"text",name:"target_date",label:s._({id:"ZmykKo"}),icon:"calendar",hidden:!t.target_date},{type:"text",name:"responsible",label:s._({id:"XQACoK"}),badge:"owner",hidden:!t.responsible}];return e.jsxs(A,{children:[e.jsxs(l,{children:[e.jsx(l.Col,{span:4,children:e.jsx(T,{appRole:N.purchase_order,apiPath:r.company_list,src:(p=t.customer_detail)==null?void 0:p.image,pk:t.customer})}),e.jsx(l.Col,{span:8,children:e.jsx(i,{fields:b,item:t})})]}),e.jsx(i,{fields:x,item:t}),e.jsx(i,{fields:j,item:t}),e.jsx(i,{fields:y,item:t})]})},[t,o]),_=d.useMemo(()=>[{name:"detail",label:s._({id:"Tol4BF"}),icon:e.jsx(h,{}),content:u},{name:"line-items",label:s._({id:"SgduFH"}),icon:e.jsx(f,{})},{name:"pending-shipments",label:s._({id:"qC/FEC"}),icon:e.jsx(g,{})},{name:"completed-shipments",label:s._({id:"polrQd"}),icon:e.jsx(k,{})},{name:"build-orders",label:s._({id:"RCVhIP"}),icon:e.jsx(I,{}),content:t!=null&&t.pk?e.jsx(Q,{salesOrderId:t.pk}):e.jsx(c,{})},{name:"attachments",label:s._({id:"w/Sphq"}),icon:e.jsx(P,{}),content:e.jsx(q,{endpoint:r.sales_order_attachment_list,model:"order",pk:Number(a)})},{name:"notes",label:s._({id:"1DBGsz"}),icon:e.jsx(C,{}),content:e.jsx(U,{url:v(r.sales_order_list,a),data:t.notes??"",allowEdit:!0})}],[t,a]);return e.jsx(e.Fragment,{children:e.jsxs(D,{spacing:"xs",children:[e.jsx(F,{visible:o.isFetching}),e.jsx(E,{title:s._({id:"LozYBo"})+`: ${t.reference}`,subtitle:t.description,imageUrl:(m=t.customer_detail)==null?void 0:m.image,breadcrumbs:[{name:s._({id:"mUv9U4"}),url:"/sales/"}]}),e.jsx(S,{pageKey:"salesorder",panels:_})]})})}export{me as default};
