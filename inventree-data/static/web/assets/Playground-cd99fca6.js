import{j as t,G as u,h as p,aI as l,r as c,o as r,S as I,aJ as M,aj as T}from"./vendor-580d7f6a.js";import{T as P}from"./BaseContext-71d55e61.js";import{O as w}from"./ApiForm-173d0ec5.js";import{P as E}from"./Placeholder-f60056df.js";import{S as b}from"./StylishText-5ee5b946.js";import{S as O}from"./Instance-4f17d9b0.js";import{A as s,M as V}from"./index-539d0685.js";import{p as D,u as S}from"./PartForms-dc889e22.js";import{u as H}from"./StockForms-2847fb41.js";import{u as g,a as d}from"./UseForm-5e9a21d6.js";import"./notifications-b554622d.js";const L=D({});function R(){const e=g({url:s.category_list,pk:2,title:"Edit Category",fields:L}),i=S({create:!0}),n=S({create:!1}),m=d({url:s.part_list,title:"Create Part",fields:i,initialData:{description:"A part created via the API"}}),x=g({url:s.part_list,pk:1,title:"Edit Part",fields:n}),h=d({url:s.part_attachment_list,title:"Create Attachment",fields:{part:{},attachment:{},comment:{}},initialData:{part:1},successMessage:"Attachment uploaded"}),[o,j]=c.useState(!0),[C,f]=c.useState("Hello"),A=c.useMemo(()=>{const a=n;return a.name={...a.name,value:C,onValueChange:f},a.active={...a.active,value:o,onValueChange:j},a.responsible={...a.responsible,disabled:!o},a},[C,o]),{modal:v,open:y}=d({url:s.part_list,title:"Create part",fields:A,initialData:{is_template:!0,virtual:!0,minimum_stock:10,description:"An example part description",keywords:"apple, banana, carrottt","initial_supplier.sku":"SKU-123"},preFormContent:t.jsx(r,{onClick:()=>f("Hello world"),children:'Set name="Hello world"'})}),{modal:F,open:_}=H();return t.jsxs(I,{children:[t.jsxs(u,{children:[t.jsx(r,{onClick:()=>m.open(),children:"Create New Part"}),m.modal,t.jsx(r,{onClick:()=>x.open(),children:"Edit Part"}),x.modal,t.jsx(r,{onClick:()=>_(),children:"Create Stock Item"}),F,t.jsx(r,{onClick:()=>e.open(),children:"Edit Category"}),e.modal,t.jsx(r,{onClick:()=>h.open(),children:"Create Attachment"}),h.modal,t.jsx(r,{onClick:()=>y(),children:"Create Part new Modal"}),v]}),t.jsx(M,{sx:{padding:"30px"},children:t.jsx(w,{props:{url:s.part_list,method:"POST",fields:{active:{value:o,onValueChange:j},keywords:{disabled:!o,value:"default,test,placeholder"}}},id:"this is very unique"})})]})}function G(){const[e,i]=c.useState("10");return t.jsx(t.Fragment,{children:t.jsxs(u,{children:[t.jsx(p,{children:"Stock Status"}),t.jsx(T,{value:e,onChange:n=>i(n.currentTarget.value)}),t.jsx(O,{type:V.stockitem,status:e})]})})}function k({title:e,content:i}){return t.jsx(t.Fragment,{children:t.jsxs(l.Item,{value:`accordion-playground-${e}`,children:[t.jsx(l.Control,{children:t.jsx(p,{children:e})}),t.jsx(l.Panel,{children:i})]})})}function X(){return t.jsxs(t.Fragment,{children:[t.jsxs(u,{children:[t.jsx(b,{children:t.jsx(P,{id:"0LrFTO"})}),t.jsx(E,{})]}),t.jsx(p,{children:t.jsx(P,{id:"ZLvUR5"})}),t.jsxs(l,{defaultValue:"",children:[t.jsx(k,{title:"API Forms",content:t.jsx(R,{})}),t.jsx(k,{title:"Status labels",content:t.jsx(G,{})})]})]})}export{X as default};