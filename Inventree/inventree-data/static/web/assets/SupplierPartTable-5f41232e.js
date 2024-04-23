import{r as n,j as i,i as s,h as _}from"./vendor-580d7f6a.js";import{A as F}from"./AddItemButton-9bde5586.js";import{T as c}from"./Instance-4f17d9b0.js";import{a as v,A as u,U as m,i as A,M as C}from"./index-539d0685.js";import{a as d}from"./CompanyForms-f616143f.js";import{a as S,b as j}from"./ApiForm-173d0ec5.js";import{g as M}from"./urls-9eea01e5.js";import{a as R}from"./UseForm-5e9a21d6.js";import{u as w,R as D,a as E,I as U}from"./InvenTreeTable-7dffc519.js";import{P as y,D as N,e as b,L as I,N as L}from"./ColumnRenderers-c7f5177c.js";import{u as O}from"./DesktopAppView-f36ad07f.js";function Z({params:a}){const l=w("supplierparts"),r=v(),k=O(),f=n.useMemo(()=>[{accessor:"part",switchable:"part"in a,sortable:!0,render:e=>y(e==null?void 0:e.part_detail)},{accessor:"supplier",sortable:!0,render:e=>{let t=(e==null?void 0:e.supplier_detail)??{};return t!=null&&t.pk?i.jsx(c,{src:(t==null?void 0:t.thumbnail)??t.image,text:t.name}):"-"}},{accessor:"SKU",title:s._({id:"nne72x"}),sortable:!0},N({}),{accessor:"manufacturer",sortable:!0,render:e=>{let t=(e==null?void 0:e.manufacturer_detail)??{};return t!=null&&t.pk?i.jsx(c,{src:(t==null?void 0:t.thumbnail)??t.image,text:t.name}):"-"}},{accessor:"MPN",sortable:!0,title:s._({id:"TOxiOu"}),render:e=>{var t;return(t=e==null?void 0:e.manufacturer_part_detail)==null?void 0:t.MPN}},{accessor:"in_stock",sortable:!0},{accessor:"packaging",sortable:!0},{accessor:"pack_quantity",sortable:!0,render:e=>{let t=(e==null?void 0:e.part_detail)??{},o=[];return t.units&&o.push(i.jsxs(_,{children:[s._({id:"v9F5VO"})," : ",t.units]},"base")),i.jsx(b,{value:e.pack_quantity,extra:o,title:s._({id:"J9LTXQ"})})}},I(),L(),{accessor:"available",sortable:!0,render:e=>{let t=[];return e.availablility_updated&&t.push(i.jsxs(_,{children:[s._({id:"+b7T3G"})," : ",e.availablility_updated]})),i.jsx(b,{value:e.available,extra:t})}}],[a]),h=d({partPk:a==null?void 0:a.part,supplierPk:a==null?void 0:a.supplier,hidePart:!0}),{modal:x,open:P}=R({url:u.supplier_part_list,title:s._({id:"EREF+D"}),fields:h,onFormSuccess:l.refreshTable,successMessage:s._({id:"LjPQ/X"})}),g=n.useMemo(()=>[i.jsx(F,{tooltip:s._({id:"PsAftp"}),onClick:P})],[r]),p=d({hidePart:!0,partPk:a==null?void 0:a.part}),T=n.useCallback(e=>[D({hidden:!r.hasChangeRole(m.purchase_order),onClick:()=>{e.pk&&S({url:u.supplier_part_list,pk:e.pk,title:s._({id:"qZstuw"}),fields:p,onFormSuccess:l.refreshTable,successMessage:s._({id:"mwOWRa"})})}}),E({hidden:!r.hasDeleteRole(m.purchase_order),onClick:()=>{e.pk&&j({url:u.supplier_part_list,pk:e.pk,title:s._({id:"9Qoago"}),successMessage:s._({id:"3GcBv9"}),onFormSuccess:l.refreshTable,preFormWarning:s._({id:"YGIkv1"})})}})],[r,p]);return i.jsxs(i.Fragment,{children:[x,i.jsx(U,{url:A(u.supplier_part_list),tableState:l,columns:f,props:{params:{...a,part_detail:!0,supplier_detail:!0,manufacturer_detail:!0},rowActions:T,tableActions:g,onRowClick:e=>{e!=null&&e.pk&&k(M(C.supplierpart,e.pk))}}})]})}export{Z as S};
