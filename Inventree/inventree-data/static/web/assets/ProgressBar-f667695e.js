import{r as m,j as a,S as i,h as x,cw as n}from"./vendor-580d7f6a.js";function u(e){const s=m.useMemo(()=>{let r=e.maximum??100,t=Math.max(e.value,0);return Math.min(100,t/r*100)},[e]);return a.jsxs(i,{spacing:2,style:{flexGrow:1,minWidth:"100px"},children:[e.progressLabel&&a.jsxs(x,{align:"center",size:"xs",children:[e.value," / ",e.maximum]}),a.jsx(n,{value:s,color:s<100?"orange":s>100?"blue":"green",size:"sm",radius:"xs"})]})}export{u as P};
