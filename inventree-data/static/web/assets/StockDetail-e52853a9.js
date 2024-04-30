import{x as J,r as n,i as t,j as s,G as q,h as N,ag as K,y as G,ay as U,O,cW as H,cZ as L,a3 as E,b7 as B,c_ as W,c$ as Q,d0 as $,d1 as X,b$ as Z,bf as ee,bg as te,b6 as se,d2 as ae,cY as le,bh as ie,w as ne,S as oe,m as re,af as de}from"./vendor-580d7f6a.js";import{I as ce,D as M}from"./ItemDetails-8f9834aa.js";import{D as pe,N as me}from"./MarkdownEditor-8fcb1f1c.js";import{B as ue,V as _e,L as be,U as he,A as Y,E as xe,D as ke}from"./ActionDropdown-0b7f88be.js";import{P as je}from"./PageDetail-e83b8dc6.js";import{P as fe}from"./PanelGroup-ecf19d17.js";import{S as ge}from"./StockLocationTree-19a73abe.js";import{a as V,A as p,g as z,i as S,U as y,M as j}from"./index-539d0685.js";import{b as ye}from"./StockForms-2847fb41.js";import{u as Ae}from"./UseInstance-05463349.js";import{a as Te,A as we}from"./AttachmentTable-3bae0b2b.js";import{S as Ie}from"./StockItemTable-b84d5ecc.js";import{u as Ce,R as Me,a as Se,d as De,F as ve,I as Pe}from"./InvenTreeTable-7dffc519.js";import{A as qe}from"./AddItemButton-9bde5586.js";import{P as Ee}from"./YesNoButton-cd4c504e.js";import{c as Be}from"./Instance-4f17d9b0.js";import{D as Fe,N as Re,r as Ke}from"./ColumnRenderers-c7f5177c.js";import{a as Ge,u as Ye,b as ze}from"./UseForm-5e9a21d6.js";import{a as Ne}from"./DesktopAppView-f36ad07f.js";import"./urls-9eea01e5.js";import"./ModelType-07300e1e.js";import"./ProgressBar-f667695e.js";import"./BaseContext-71d55e61.js";import"./StylishText-5ee5b946.js";import"./notifications-b554622d.js";import"./Placeholder-f60056df.js";import"./index.es-6e6e8db2.js";import"./ApiForm-173d0ec5.js";function Ue({partId:r,itemId:o}){const u=V(),m=Ce("stocktests"),{data:e}=J({queryKey:["stocktesttemplates",r,o],queryFn:async()=>r?z.get(S(p.part_test_template_list),{params:{part:r,include_inherited:!0,enabled:!0}}).then(a=>a.data).catch(a=>[]):[]});n.useEffect(()=>{m.refreshTable()},[e]);const D=n.useCallback(a=>{let l=e.map(i=>({...i,templateId:i.pk,results:[]}));return a.forEach(i=>{l.find(c=>c.templateId==i.template)||l.push({...i.template_detail,templateId:i.template,results:[]})}),a.sort((i,c)=>i.pk>c.pk?1:-1).forEach(i=>{let c=l.findIndex(C=>C.templateId==i.template);c>=0&&(l[c]={...l[c],...i},l[c].results.push(i))}),l},[r,o,e]),b=n.useMemo(()=>[{accessor:"test",title:t._({id:"NnH3pK"}),switchable:!1,sortable:!0,render:a=>{var C,F,R;let l=a.required??((C=a.template_detail)==null?void 0:C.required),i=a.enabled??((F=a.template_detail)==null?void 0:F.enabled),c=a.stock_item!=null&&a.stock_item!=o;return s.jsxs(q,{position:"apart",children:[s.jsxs(N,{italic:c,fw:l&&700,color:i?void 0:"red",children:[!a.templateId&&"- ",a.test_name??((R=a.template_detail)==null?void 0:R.test_name)]}),s.jsxs(q,{position:"right",children:[a.results&&a.results.length>1&&s.jsx(K,{label:t._({id:"isbwWo"}),children:s.jsx(G,{color:"lightblue",variant:"filled",children:a.results.length})}),c&&s.jsx(K,{label:t._({id:"yd1WJ/"}),children:s.jsx(U,{size:16,color:"blue"})})]})]})}},{accessor:"result",title:t._({id:"RD6AE9"}),switchable:!1,sortable:!0,render:a=>a.result===void 0?s.jsx(G,{color:"lightblue",variant:"filled",children:t._({id:"4bobEy"})}):s.jsx(Ee,{value:a.result})},Fe({accessor:"description"}),{accessor:"value",title:t._({id:"wMHvYH"})},{accessor:"attachment",title:t._({id:"UY1vmE"}),render:a=>a.attachment&&s.jsx(Te,{attachment:a.attachment})},Re(),{accessor:"date",sortable:!0,title:t._({id:"mYGY3B"}),render:a=>s.jsxs(q,{position:"apart",children:[Ke(a.date),a.user_detail&&s.jsx(Be,{instance:a.user_detail})]})}],[o]),A=n.useMemo(()=>({template:{filters:{include_inherited:!0,part:r}},result:{},value:{},attachment:{},notes:{},stock_item:{value:o,hidden:!0}}),[r,o]),[v,T]=n.useState(void 0),h=Ge({url:p.stock_test_result_list,fields:A,initialData:{template:v,result:!0},title:t._({id:"VzkBcq"}),onFormSuccess:()=>m.refreshTable(),successMessage:t._({id:"VivtT0"})}),[w,f]=n.useState(void 0),g=Ye({url:p.stock_test_result_list,pk:w,fields:A,title:t._({id:"1HKt5e"}),onFormSuccess:()=>m.refreshTable(),successMessage:t._({id:"G0v/SO"})}),d=ze({url:p.stock_test_result_list,pk:w,title:t._({id:"381PhV"}),onFormSuccess:()=>m.refreshTable(),successMessage:t._({id:"xbuMqN"})}),x=n.useCallback(a=>{z.post(S(p.stock_test_result_list),{template:a,stock_item:o,result:!0}).then(()=>{m.refreshTable(),O({title:t._({id:"uUlW4e"}),message:t._({id:"uiR3yF"}),color:"green"})})},[o]),_=n.useCallback(a=>a.stock_item!=null&&a.stock_item!=o?[]:[{title:t._({id:"up/ozE"}),color:"green",icon:s.jsx(H,{}),hidden:!a.templateId||(a==null?void 0:a.requires_attachment)||(a==null?void 0:a.requires_value)||a.result,onClick:()=>x(a.templateId)},{title:t._({id:"m16xKo"}),tooltip:t._({id:"VzkBcq"}),color:"green",icon:s.jsx(L,{}),hidden:!u.hasAddRole(y.stock)||!a.templateId,onClick:()=>{T(a.templateId),h.open()}},Me({tooltip:t._({id:"1HKt5e"}),hidden:!u.hasChangeRole(y.stock)||!a.template_detail,onClick:()=>{f(a.pk),g.open()}}),Se({tooltip:t._({id:"381PhV"}),hidden:!u.hasDeleteRole(y.stock)||!a.template_detail,onClick:()=>{f(a.pk),d.open()}})],[u,o]),k=n.useMemo(()=>[{name:"required",label:t._({id:"TMLAx2"}),description:t._({id:"sKK8za"})},{name:"include_installed",label:t._({id:"TD72EF"}),description:t._({id:"BYeSw1"})},{name:"result",label:t._({id:"nqMwPi"}),description:t._({id:"bcwRe2"})}],[]),P=n.useMemo(()=>[s.jsx(qe,{tooltip:t._({id:"VzkBcq"}),onClick:()=>{T(void 0),h.open()},hidden:!u.hasAddRole(y.stock)})],[u]),I=n.useMemo(()=>{const a=[...b,{accessor:"actions",title:"  ",hidden:!1,switchable:!1,width:50,render:l=>s.jsx(De,{actions:_(l)??[]})}];return{allowMultiple:!0,content:({record:l})=>{if(!l||!l.results||l.results.length<2)return null;const i=(l==null?void 0:l.results)??[];return s.jsx(ve,{noHeader:!0,columns:a,records:i.slice(0,-1)},l.pk)}}},[]);return s.jsxs(s.Fragment,{children:[h.modal,g.modal,d.modal,s.jsx(Pe,{url:S(p.stock_test_result_list),tableState:m,columns:b,props:{dataFormatter:D,enablePagination:!1,tableActions:P,tableFilters:k,rowActions:_,rowExpansion:I,params:{stock_item:o,user_detail:!0,attachment_detail:!0,template_detail:!0,enabled:!0}}})]})}function kt(){var f,g;const{id:r}=Ne(),o=V(),[u,m]=n.useState(!1),{instance:e,refreshInstance:D,instanceQuery:b}=Ae({endpoint:p.stock_item_list,pk:r,params:{part_detail:!0,location_detail:!0,path_detail:!0}}),A=n.useMemo(()=>{var I,a;let d=e;if(d.available_stock=Math.max(0,d.quantity-d.allocated),b.isFetching)return s.jsx(E,{});let x=[{name:"part",label:t._({id:"mY+KgP"}),type:"link",model:j.part},{name:"status",type:"text",label:t._({id:"Y3/0dR"})},{type:"text",name:"tests",label:"Completed Tests",icon:"progress"},{type:"text",name:"updated",icon:"calendar",label:t._({id:"K7P0jz"})},{type:"text",name:"stocktake",icon:"calendar",label:t._({id:"whZ7zT"}),hidden:!e.stocktake}],_=[{type:"text",name:"quantity",label:t._({id:"VbWX2u"})},{type:"text",name:"serial",label:t._({id:"AXeJt4"}),hidden:!e.serial},{type:"text",name:"available_stock",label:t._({id:"csDS2L"})}],k=[{name:"supplier_part",label:t._({id:"nne72x"}),type:"link",model:j.supplierpart,hidden:!e.supplier_part},{type:"link",name:"location",label:t._({id:"wJijgU"}),model:j.stocklocation,hidden:!e.location},{type:"link",name:"belongs_to",label:t._({id:"QPoAhl"}),model:j.stockitem,hidden:!e.belongs_to},{type:"link",name:"consumed_by",label:t._({id:"H00rnl"}),model:j.build,hidden:!e.consumed_by},{type:"link",name:"sales_order",label:t._({id:"LozYBo"}),model:j.salesorder,hidden:!e.sales_order}],P=[{type:"text",name:"packaging",icon:"part",label:t._({id:"pD/Ew0"}),hidden:!e.packaging}];return s.jsxs(ce,{children:[s.jsxs(B,{children:[s.jsx(B.Col,{span:4,children:s.jsx(pe,{appRole:y.part,apiPath:p.part_list,src:((I=e.part_detail)==null?void 0:I.image)??((a=e==null?void 0:e.part_detail)==null?void 0:a.thumbnail),pk:e.part})}),s.jsx(B.Col,{span:8,children:s.jsx(M,{fields:x,item:e})})]}),s.jsx(M,{fields:_,item:e}),s.jsx(M,{fields:k,item:e}),s.jsx(M,{fields:P,item:e})]})},[e,b]),v=n.useMemo(()=>{var d,x,_,k;return[{name:"details",label:t._({id:"hBG+yp"}),icon:s.jsx(U,{}),content:A},{name:"tracking",label:t._({id:"IdrYoA"}),icon:s.jsx(W,{})},{name:"allocations",label:t._({id:"KwhnxF"}),icon:s.jsx(Q,{}),hidden:!((d=e==null?void 0:e.part_detail)!=null&&d.salable)&&!((x=e==null?void 0:e.part_detail)!=null&&x.component)},{name:"testdata",label:t._({id:"dljGeD"}),icon:s.jsx($,{}),hidden:!((_=e==null?void 0:e.part_detail)!=null&&_.trackable),content:e!=null&&e.pk?s.jsx(Ue,{itemId:e.pk,partId:e.part}):s.jsx(E,{})},{name:"installed_items",label:t._({id:"xnskHi"}),icon:s.jsx(X,{}),hidden:!((k=e==null?void 0:e.part_detail)!=null&&k.assembly)},{name:"child_items",label:t._({id:"K4v96J"}),icon:s.jsx(Z,{}),hidden:((e==null?void 0:e.child_items)??0)==0,content:e!=null&&e.pk?s.jsx(Ie,{params:{ancestor:e.pk}}):s.jsx(E,{})},{name:"attachments",label:t._({id:"w/Sphq"}),icon:s.jsx(ee,{}),content:s.jsx(we,{endpoint:p.stock_attachment_list,model:"stock_item",pk:Number(r)})},{name:"notes",label:t._({id:"1DBGsz"}),icon:s.jsx(te,{}),content:s.jsx(me,{url:S(p.stock_item_list,r),data:e.notes??"",allowEdit:!0})}]},[e,r]),T=n.useMemo(()=>[{name:t._({id:"blbbPS"}),url:"/stock"},...(e.location_path??[]).map(d=>({name:d.name,url:`/stock/location/${d.pk}`}))],[e]),h=ye({item_id:e.pk,callback:()=>D()}),w=n.useMemo(()=>[s.jsx(ue,{actions:[_e({}),be({disabled:e==null?void 0:e.barcode_hash}),he({disabled:!(e!=null&&e.barcode_hash)})]}),s.jsx(Y,{tooltip:t._({id:"ClJC3x"}),icon:s.jsx(se,{}),actions:[{name:t._({id:"wBMjJ2"}),tooltip:t._({id:"rb0Klh"}),icon:s.jsx(H,{color:"green"})},{name:t._({id:"m16xKo"}),tooltip:t._({id:"vq/m8u"}),icon:s.jsx(L,{color:"green"})},{name:t._({id:"t/YqKh"}),tooltip:t._({id:"qpe+W0"}),icon:s.jsx(ae,{color:"red"})},{name:t._({id:"zPGNJm"}),tooltip:t._({id:"+OxnAC"}),icon:s.jsx(le,{color:"blue"})}]},"operations"),s.jsx(Y,{icon:s.jsx(ie,{}),actions:[{name:t._({id:"euc6Ns"}),tooltip:t._({id:"KD3GYK"}),icon:s.jsx(ne,{})},xe({onClick:()=>{e.pk&&h.open()}}),ke({})]},"stock")],[r,e,o]);return s.jsxs(oe,{children:[s.jsx(re,{visible:b.isFetching}),s.jsx(ge,{opened:u,onClose:()=>m(!1),selectedLocation:e==null?void 0:e.location}),s.jsx(je,{title:t._({id:"igx8Og"}),subtitle:(f=e.part_detail)==null?void 0:f.full_name,imageUrl:(g=e.part_detail)==null?void 0:g.thumbnail,detail:s.jsx(de,{color:"teal",title:"Stock Item",children:s.jsxs(N,{children:["Quantity: ",e.quantity??"idk"]})}),breadcrumbs:T,breadcrumbAction:()=>{m(!0)},actions:w}),s.jsx(fe,{pageKey:"stockitem",panels:v}),h.modal]})}export{kt as default};