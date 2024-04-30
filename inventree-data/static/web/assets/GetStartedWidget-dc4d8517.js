import{r as z,cj as ar,Z as Oe,d$ as He,aN as ie,_ as k,e0 as qe,R as X,B as We,aO as ir,aP as or,a2 as be,aM as Te,j as F,ap as sr,T as Ke,h as lr,A as cr,o as ur}from"./vendor-580d7f6a.js";import{T as Ue}from"./BaseContext-71d55e61.js";import{n as dr}from"./links-65930103.js";import{P as fr}from"./Placeholder-f60056df.js";import"./index-539d0685.js";import"./StylishText-5ee5b946.js";function vr(e,r,n,t,i){return t+(i-t)*((e-r)/(n-r))}function _e(e){return typeof e=="number"}function De(e){return typeof e=="string"}function Ce(e){return Object.prototype.toString.call(e)==="[object Object]"}function pr(e){return Array.isArray(e)}function ke(e){return Ce(e)||pr(e)}function N(e){return Math.abs(e)}function Ae(e){return e?e/N(e):0}function ue(e,r){return N(e-r)}function mr(e,r){if(e===0||r===0||N(e)<=N(r))return 0;var n=ue(N(e),N(r));return N(n/e)}function gr(e){var r=Math.pow(10,e);return function(n){return Math.round(n*r)/r}}function de(e){return se(e).map(Number)}function ee(e){return e[ye(e)]}function ye(e){return Math.max(0,e.length-1)}function se(e){return Object.keys(e)}function Je(e,r){return[e,r].reduce(function(n,t){return se(t).forEach(function(i){var s=n[i],o=t[i],d=Ce(s)&&Ce(o);n[i]=d?Je(s,o):o}),n},{})}function Xe(e,r){var n=se(e),t=se(r);return n.length!==t.length?!1:n.every(function(i){var s=e[i],o=r[i];return typeof s=="function"?"".concat(s)==="".concat(o):!ke(s)||!ke(o)?s===o:Xe(s,o)})}function hr(e,r){var n={start:t,center:i,end:s};function t(){return 0}function i(u){return s(u)/2}function s(u){return r-u}function o(){return r*Number(e)}function d(u){return _e(e)?o():n[e](u)}var c={measure:d};return c}function Sr(e){var r=0;function n(o,d){return function(){o===!!r&&d()}}function t(){r=window.requestAnimationFrame(e)}function i(){window.cancelAnimationFrame(r),r=0}var s={proceed:n(!0,t),start:n(!1,t),stop:n(!0,i)};return s}function yr(e,r){var n=e==="y"?"y":"x",t=e==="y"?"x":"y",i=d(),s=c();function o(l){var a=l.width,f=l.height;return n==="x"?a:f}function d(){return n==="y"?"top":r==="rtl"?"right":"left"}function c(){return n==="y"?"bottom":r==="rtl"?"left":"right"}var u={scroll:n,cross:t,startEdge:i,endEdge:s,measureSize:o};return u}function ce(e,r){var n=N(e-r);function t(u){return u<e}function i(u){return u>r}function s(u){return t(u)||i(u)}function o(u){return s(u)?t(u)?e:r:u}function d(u){return n?u-n*Math.ceil((u-r)/n):u}var c={length:n,max:r,min:e,constrain:o,reachedAny:s,reachedMax:i,reachedMin:t,removeOffset:d};return c}function Qe(e,r,n){var t=ce(0,e),i=t.min,s=t.constrain,o=e+1,d=c(r);function c(p){return n?N((o+p)%o):s(p)}function u(){return d}function l(p){return d=c(p),v}function a(p){return l(u()+p)}function f(){return Qe(e,u(),n)}var v={add:a,clone:f,get:u,set:l,min:i,max:e};return v}function xr(e){var r=e==="rtl"?-1:1;function n(i){return i*r}var t={apply:n};return t}function ge(){var e=[];function r(i,s,o,d){return d===void 0&&(d={passive:!0}),i.addEventListener(s,o,d),e.push(function(){return i.removeEventListener(s,o,d)}),t}function n(){return e=e.filter(function(i){return i()}),t}var t={add:r,removeAll:n};return t}function oe(e){var r=e;function n(){return r}function t(a){return r=u(a),l}function i(a){return r+=u(a),l}function s(a){return r-=u(a),l}function o(a){return r*=a,l}function d(a){return r/=a,l}function c(){return r!==0&&d(r),l}function u(a){return _e(a)?a:a.get()}var l={add:i,divide:d,get:n,multiply:o,normalize:c,set:t,subtract:s};return l}function wr(e,r,n,t,i,s,o,d,c,u,l,a,f,v,p,b){var x=e.cross,g=["INPUT","SELECT","TEXTAREA"],m={passive:!1},E=oe(0),w=ge(),y=ge(),P=f.measure(20),O={mouse:300,touch:400},_={mouse:500,touch:600},T=p?5:16,H=1,R=0,Q=0,U=!1,W=!1,G=!1,A=!1;function Z(){var S=n;w.add(S,"dragstart",function(D){return D.preventDefault()},m).add(S,"touchmove",function(){},m).add(S,"touchend",function(){}).add(S,"touchstart",te).add(S,"mousedown",te).add(S,"touchcancel",K).add(S,"contextmenu",K).add(S,"click",j,!0)}function L(){var S=A?document:n;y.add(S,"touchmove",M,m).add(S,"touchend",K).add(S,"mousemove",M,m).add(S,"mouseup",K)}function q(){w.removeAll(),y.removeAll()}function Y(S){var D=S.nodeName||"";return g.indexOf(D)>-1}function re(){var S=p?_:O,D=A?"mouse":"touch";return S[D]}function ne(S,D){var V=l.clone().add(Ae(S)*-1),I=V.get()===l.min||V.get()===l.max,$=u.byDistance(S,!p).distance;return p||N(S)<P?$:!v&&I?$*.4:b&&D?$*.5:u.byIndex(V.get(),0).distance}function te(S){if(A=!i.isTouchEvent(S),!(A&&S.button!==0)&&!Y(S.target)){var D=ue(t.get(),s.get())>=2,V=A||!D;U=!0,i.pointerDown(S),E.set(t),t.set(s),c.useBaseMass().useSpeed(80),L(),R=i.readPoint(S),Q=i.readPoint(S,x),a.emit("pointerDown"),V&&(G=!1)}}function M(S){if(!W&&!A){if(!S.cancelable)return K(S);var D=i.readPoint(S),V=i.readPoint(S,x),I=ue(D,R),$=ue(V,Q);if(W=I>$,!W&&!G)return K(S)}var ae=i.pointerMove(S);!G&&ae&&(G=!0),o.start(),t.add(r.apply(ae)),S.preventDefault()}function K(S){var D=u.byDistance(0,!1),V=D.index!==l.get(),I=i.pointerUp(S)*re(),$=ne(r.apply(I),V),ae=mr(I,$),fe=ue(t.get(),E.get())>=.5,ve=V&&ae>.75,pe=N(I)<P,me=ve?10:T,xe=ve?H+2.5*ae:H;fe&&!A&&(G=!0),W=!1,U=!1,y.removeAll(),c.useSpeed(pe?9:me).useMass(xe),d.distance($,!p),A=!1,a.emit("pointerUp")}function j(S){G&&(S.stopPropagation(),S.preventDefault())}function C(){return!G}function h(){return U}var B={addActivationEvents:Z,clickAllowed:C,pointerDown:h,removeAllEvents:q};return B}function br(e){var r=170,n,t;function i(a){return typeof TouchEvent<"u"&&a instanceof TouchEvent}function s(a){return a.timeStamp}function o(a,f){var v=f||e.scroll,p="client".concat(v==="x"?"X":"Y");return(i(a)?a.touches[0]:a)[p]}function d(a){return n=a,t=a,o(a)}function c(a){var f=o(a)-o(t),v=s(a)-s(n)>r;return t=a,v&&(n=a),f}function u(a){if(!n||!t)return 0;var f=o(t)-o(n),v=s(a)-s(n),p=s(a)-s(t)>r,b=f/v,x=v&&!p&&N(b)>.1;return x?b:0}var l={isTouchEvent:i,pointerDown:d,pointerMove:c,pointerUp:u,readPoint:o};return l}function Er(e){function r(t){return e*(t/100)}var n={measure:r};return n}function Pr(e,r,n){var t=gr(2),i=oe(0),s=oe(0),o=oe(0),d=0,c=r,u=n;function l(){i.add(s),e.add(i),s.multiply(0)}function a(w){w.divide(u),s.add(w)}function f(w){o.set(w).subtract(e);var y=vr(o.get(),0,100,0,c);return d=Ae(o.get()),o.normalize().multiply(y).subtract(i),a(o),E}function v(w){var y=w.get()-e.get(),P=!t(y);return P&&e.set(w),P}function p(){return d}function b(){return g(r)}function x(){return m(n)}function g(w){return c=w,E}function m(w){return u=w,E}var E={direction:p,seek:f,settle:v,update:l,useBaseMass:x,useBaseSpeed:b,useMass:m,useSpeed:g};return E}function Cr(e,r,n,t,i){var s=i.measure(10),o=i.measure(50),d=.85,c=!1;function u(){return!(c||!e.reachedAny(n.get())||!e.reachedAny(r.get()))}function l(v){if(u()){var p=e.reachedMin(r.get())?"min":"max",b=N(e[p]-r.get()),x=n.get()-r.get(),g=Math.min(b/o,d);n.subtract(x*g),!v&&N(x)<s&&(n.set(e.constrain(n.get())),t.useSpeed(10).useMass(3))}}function a(v){c=!v}var f={constrain:l,toggleActive:a};return f}function Or(e,r,n,t){var i=ce(-r+e,n[0]),s=n.map(i.constrain),o=c();function d(){var l=s[0],a=ee(s),f=s.lastIndexOf(l),v=s.indexOf(a)+1;return ce(f,v)}function c(){if(r<=e)return[i.max];if(t==="keepSnaps")return s;var l=d(),a=l.min,f=l.max;return s.slice(a,f)}var u={snapsContained:o};return u}function _r(e,r,n){var t=i();function i(){var o=r[0],d=ee(r),c=n?o-e:d,u=o;return ce(c,u)}var s={limit:t};return s}function Ar(e,r,n,t){var i=.1,s=r.min+i,o=r.max+i,d=ce(s,o),c=d.reachedMin,u=d.reachedMax;function l(v){return v===1?u(n.get()):v===-1?c(n.get()):!1}function a(v){if(l(v)){var p=e*(v*-1);t.forEach(function(b){return b.add(p)})}}var f={loop:a};return f}function Ir(e){var r=e.max,n=e.length;function t(s){var o=s-r;return o/-n}var i={get:t};return i}function zr(e,r,n,t,i,s,o){var d=e.startEdge,c=e.endEdge,u=s.groupSlides,l=v().map(r.measure),a=p(),f=b();function v(){return u(t).map(function(g){return ee(g)[c]-g[0][d]}).map(N)}function p(){return t.map(function(g){return n[d]-g[d]}).map(function(g){return-N(g)})}function b(){var g=0,m=ee(a)-ee(i);return u(a).map(function(E){return E[0]}).map(function(E,w,y){var P=!w,O=w===ye(y);return o&&P?g:o&&O?m:E+l[w]})}var x={snaps:a,snapsAligned:f};return x}function Nr(e,r,n,t,i){var s=t.reachedAny,o=t.removeOffset,d=t.constrain;function c(p){return p.concat().sort(function(b,x){return N(b)-N(x)})[0]}function u(p){var b=e?o(p):d(p),x=r.map(function(m){return m-b}).map(function(m){return l(m,0)}).map(function(m,E){return{diff:m,index:E}}).sort(function(m,E){return N(m.diff)-N(E.diff)}),g=x[0].index;return{index:g,distance:b}}function l(p,b){var x=[p,p+n,p-n];if(!e)return x[0];if(!b)return c(x);var g=x.filter(function(m){return Ae(m)===b});return c(g)}function a(p,b){var x=r[p]-i.get(),g=l(x,b);return{index:p,distance:g}}function f(p,b){var x=i.get()+p,g=u(x),m=g.index,E=g.distance,w=!e&&s(x);if(!b||w)return{index:m,distance:p};var y=r[m]-E,P=p+l(y,0);return{index:m,distance:P}}var v={byDistance:f,byIndex:a,shortcut:l};return v}function Tr(e,r,n,t,i,s){function o(l){var a=l.distance,f=l.index!==r.get();a&&(e.start(),i.add(a)),f&&(n.set(r.get()),r.set(l.index),s.emit("select"))}function d(l,a){var f=t.byDistance(l,a);o(f)}function c(l,a){var f=r.clone().set(l),v=t.byIndex(f.get(),a);o(v)}var u={distance:d,index:c};return u}function Ye(e,r,n){var t=e.scroll==="x"?o:d,i=n.style,s=!1;function o(f){return"translate3d(".concat(f,"px,0px,0px)")}function d(f){return"translate3d(0px,".concat(f,"px,0px)")}function c(f){s||(i.transform=t(r.apply(f.get())))}function u(f){s=!f}function l(){s||(i.transform="",n.getAttribute("style")||n.removeAttribute("style"))}var a={clear:l,to:c,toggleActive:u};return a}function Dr(e,r,n,t,i,s,o,d,c){var u=de(i),l=de(i).reverse(),a=b().concat(x());function f(y,P){return y.reduce(function(O,_){return O-i[_]},P)}function v(y,P){return y.reduce(function(O,_){var T=f(O,P);return T>0?O.concat([_]):O},[])}function p(y,P){var O=P==="start",_=O?-t:t,T=o.findSlideBounds([_]);return y.map(function(H){var R=O?0:-t,Q=O?t:0,U=T.filter(function(q){return q.index===H})[0],W=U[O?"end":"start"],G=oe(-1),A=oe(-1),Z=Ye(e,r,c[H]),L=function(){return G.set(d.get()>W?R:Q)};return{index:H,location:A,translate:Z,target:L}})}function b(){var y=s[0]-1,P=v(l,y);return p(P,"end")}function x(){var y=n-s[0]-1,P=v(u,y);return p(P,"start")}function g(){return a.every(function(y){var P=y.index,O=u.filter(function(_){return _!==P});return f(O,n)<=.1})}function m(){a.forEach(function(y){var P=y.target,O=y.translate,_=y.location,T=P();T.get()!==_.get()&&(T.get()===0?O.clear():O.to(T),_.set(T))})}function E(){a.forEach(function(y){return y.translate.clear()})}var w={canLoop:g,clear:E,loop:m,loopPoints:a};return w}function kr(e,r,n,t,i,s,o){var d=i.removeOffset,c=i.constrain,u=.5,l=s?[0,r,-r]:[0],a=v(l,o);function f(x){var g=x||0;return n.map(function(m){var E=ce(u,m-u);return E.constrain(m*g)})}function v(x,g){var m=x||l,E=f(g);return m.reduce(function(w,y){var P=t.map(function(O,_){return{start:O-n[_]+E[_]+y,end:O+e-E[_]+y,index:_}});return w.concat(P)},[])}function p(x,g){var m=s?d(x):c(x),E=g||a;return E.reduce(function(w,y){var P=y.index,O=y.start,_=y.end,T=w.indexOf(P)!==-1,H=O<m&&_>m;return!T&&H?w.concat([P]):w},[])}var b={check:p,findSlideBounds:v};return b}function Br(e,r,n,t,i){var s=e.measureSize,o=e.startEdge,d=e.endEdge,c=n[0]&&i,u=v(),l=p(),a=n.map(s),f=b();function v(){if(!c)return 0;var g=n[0];return N(r[o]-g[o])}function p(){if(!c)return 0;var g=window.getComputedStyle(ee(t));return parseFloat(g.getPropertyValue("margin-".concat(d)))}function b(){return n.map(function(g,m,E){var w=!m,y=m===ye(E);return w?a[m]+u:y?a[m]+l:E[m+1][o]-g[o]}).map(N)}var x={slideSizes:a,slideSizesWithGaps:f};return x}function Lr(e,r,n){var t=_e(n);function i(c,u){return de(c).filter(function(l){return l%u===0}).map(function(l){return c.slice(l,l+u)})}function s(c){return de(c).reduce(function(u,l){var a=r.slice(ee(u),l+1),f=a.reduce(function(v,p){return v+p},0);return!l||f>e?u.concat(l):u},[]).map(function(u,l,a){return c.slice(u,a[l+1])})}function o(c){return t?i(c,n):s(c)}var d={groupSlides:o};return d}function Mr(e,r,n,t,i){var s=t.align,o=t.axis,d=t.direction,c=t.startIndex,u=t.inViewThreshold,l=t.loop,a=t.speed,f=t.dragFree,v=t.slidesToScroll,p=t.skipSnaps,b=t.containScroll,x=r.getBoundingClientRect(),g=n.map(function($){return $.getBoundingClientRect()}),m=xr(d),E=yr(o,d),w=E.measureSize(x),y=Er(w),P=hr(s,w),O=!l&&b!=="",_=l||b!=="",T=Br(E,x,g,n,_),H=T.slideSizes,R=T.slideSizesWithGaps,Q=Lr(w,R,v),U=zr(E,P,x,g,R,Q,O),W=U.snaps,G=U.snapsAligned,A=-ee(W)+ee(R),Z=Or(w,A,G,b).snapsContained,L=O?Z:G,q=_r(A,L,l).limit,Y=Qe(ye(L),c,l),re=Y.clone(),ne=de(n),te=function(){l||I.scrollBounds.constrain(I.dragHandler.pointerDown()),I.scrollBody.seek(C).update();var $=I.scrollBody.settle(C);$&&!I.dragHandler.pointerDown()&&(I.animation.stop(),i.emit("settle")),$||i.emit("scroll"),l&&(I.scrollLooper.loop(I.scrollBody.direction()),I.slideLooper.loop()),I.translate.to(j),I.animation.proceed()},M=Sr(te),K=L[Y.get()],j=oe(K),C=oe(K),h=Pr(j,a,1),B=Nr(l,L,A,q,C),S=Tr(M,Y,re,B,C,i),D=kr(w,A,H,W,q,l,u),V=wr(E,m,e,C,br(E),j,M,S,h,B,Y,i,y,l,f,p),I={containerRect:x,slideRects:g,animation:M,axis:E,direction:m,dragHandler:V,eventStore:ge(),percentOfView:y,index:Y,indexPrevious:re,limit:q,location:j,options:t,scrollBody:h,scrollBounds:Cr(q,j,C,h,y),scrollLooper:Ar(A,q,j,[j,C]),scrollProgress:Ir(q),scrollSnaps:L,scrollTarget:B,scrollTo:S,slideLooper:Dr(E,m,w,A,R,L,D,j,n),slidesToScroll:Q,slidesInView:D,slideIndexes:ne,target:C,translate:Ye(E,m,r)};return I}function jr(){var e={};function r(o){return e[o]||[]}function n(o){return r(o).forEach(function(d){return d(o)}),s}function t(o,d){return e[o]=r(o).concat([d]),s}function i(o,d){return e[o]=r(o).filter(function(c){return c!==d}),s}var s={emit:n,off:i,on:t};return s}var $r={align:"center",axis:"x",container:null,slides:null,containScroll:"",direction:"ltr",slidesToScroll:1,breakpoints:{},dragFree:!1,draggable:!0,inViewThreshold:0,loop:!1,skipSnaps:!1,speed:10,startIndex:0,active:!0};function Ie(){function e(i,s){return Je(i,s||{})}function r(i,s){var o=JSON.stringify(se(i.breakpoints||{})),d=JSON.stringify(se(s.breakpoints||{}));return o!==d?!1:Xe(i,s)}function n(i){var s=i.breakpoints||{},o=se(s).filter(function(d){return window.matchMedia(d).matches}).map(function(d){return s[d]}).reduce(function(d,c){return e(d,c)},{});return e(i,o)}var t={merge:e,areEqual:r,atMedia:n};return t}function Gr(){var e=Ie(),r=e.atMedia,n=e.areEqual,t=[],i=[];function s(){return i.some(function(l){return l()})}function o(l){var a=r(l.options);return function(){return!n(a,r(l.options))}}function d(l,a){return i=l.map(o),t=l.filter(function(f){return r(f.options).active}),t.forEach(function(f){return f.init(a)}),l.reduce(function(f,v){var p;return Object.assign(f,(p={},p[v.name]=v,p))},{})}function c(){t=t.filter(function(l){return l.destroy()})}var u={init:d,destroy:c,haveChanged:s};return u}function le(e,r,n){var t=ge(),i=Ie(),s=Gr(),o=jr(),d=o.on,c=o.off,u=y,l=!1,a,f=i.merge($r,le.globalOptions),v=i.merge(f),p=[],b,x=0,g,m;function E(){var C=v.container,h=v.slides,B=De(C)?e.querySelector(C):C;g=B||e.children[0];var S=De(h)?g.querySelectorAll(h):h;m=[].slice.call(S||g.children)}function w(C,h){if(!l){if(f=i.merge(f,C),v=i.atMedia(f),E(),a=Mr(e,g,m,v,o),x=a.axis.measureSize(e.getBoundingClientRect()),!v.active)return P();if(a.translate.to(a.location),p=h||p,b=s.init(p,j),v.loop){if(!a.slideLooper.canLoop()){P(),w({loop:!1},h),f=i.merge(f,{loop:!0});return}a.slideLooper.loop()}v.draggable&&g.offsetParent&&m.length&&a.dragHandler.addActivationEvents()}}function y(C,h){var B=L();P(),w(i.merge({startIndex:B},C),h),o.emit("reInit")}function P(){a.dragHandler.removeAllEvents(),a.animation.stop(),a.eventStore.removeAll(),a.translate.clear(),a.slideLooper.clear(),s.destroy()}function O(){l||(l=!0,t.removeAll(),P(),o.emit("destroy"))}function _(){var C=i.atMedia(f),h=!i.areEqual(C,v),B=a.axis.measureSize(e.getBoundingClientRect()),S=x!==B,D=s.haveChanged();(S||h||D)&&y(),o.emit("resize")}function T(C){var h=a[C?"target":"location"].get(),B=v.loop?"removeOffset":"constrain";return a.slidesInView.check(a.limit[B](h))}function H(C){var h=T(C);return a.slideIndexes.filter(function(B){return h.indexOf(B)===-1})}function R(C,h,B){!v.active||l||(a.scrollBody.useBaseMass().useSpeed(h?100:v.speed),a.scrollTo.index(C,B||0))}function Q(C){var h=a.index.clone().add(1);R(h.get(),C===!0,-1)}function U(C){var h=a.index.clone().add(-1);R(h.get(),C===!0,1)}function W(){var C=a.index.clone().add(1);return C.get()!==L()}function G(){var C=a.index.clone().add(-1);return C.get()!==L()}function A(){return a.scrollSnaps.map(a.scrollProgress.get)}function Z(){return a.scrollProgress.get(a.location.get())}function L(){return a.index.get()}function q(){return a.indexPrevious.get()}function Y(){return a.dragHandler.clickAllowed()}function re(){return b}function ne(){return a}function te(){return e}function M(){return g}function K(){return m}var j={canScrollNext:W,canScrollPrev:G,clickAllowed:Y,containerNode:M,internalEngine:ne,destroy:O,off:c,on:d,plugins:re,previousScrollSnap:q,reInit:u,rootNode:te,scrollNext:Q,scrollPrev:U,scrollProgress:Z,scrollSnapList:A,scrollTo:R,selectedScrollSnap:L,slideNodes:K,slidesInView:T,slidesNotInView:H};return w(r,n),t.add(window,"resize",_),setTimeout(function(){return o.emit("init")},0),j}le.globalOptions=void 0;le.optionsHandler=Ie;function Rr(){return!!(typeof window<"u"&&window.document&&window.document.createElement)}function Be(e){return e.concat().sort(function(r,n){return r.name>n.name?1:-1}).map(function(r){return r.options})}function Vr(e,r){if(e.length!==r.length)return!1;var n=le.optionsHandler().areEqual,t=Be(e),i=Be(r);return t.every(function(s,o){var d=i[o];return n(s,d)})}function ze(e,r){e===void 0&&(e={}),r===void 0&&(r=[]);var n=z.useRef(le.optionsHandler()),t=z.useRef(e),i=z.useRef(r),s=z.useState(),o=s[0],d=s[1],c=z.useState(),u=c[0],l=c[1],a=z.useCallback(function(){o&&o.reInit(t.current,i.current)},[o]);return z.useEffect(function(){if(Rr()&&u){le.globalOptions=ze.globalOptions;var f=le(u,t.current,i.current);return d(f),function(){return f.destroy()}}else d(void 0)},[u,d]),z.useEffect(function(){n.current.areEqual(t.current,e)||(t.current=e,a())},[e,a]),z.useEffect(function(){Vr(i.current,r)||(i.current=r,a())},[r,a]),[l,o]}ze.globalOptions=void 0;const Fr={context:"[@mantine/carousel] Carousel.Slide was rendered outside of Carousel context"},[Hr,qr]=ar(Fr.context);var Wr=Object.defineProperty,Kr=Object.defineProperties,Ur=Object.getOwnPropertyDescriptors,Le=Object.getOwnPropertySymbols,Jr=Object.prototype.hasOwnProperty,Xr=Object.prototype.propertyIsEnumerable,Me=(e,r,n)=>r in e?Wr(e,r,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[r]=n,Ee=(e,r)=>{for(var n in r||(r={}))Jr.call(r,n)&&Me(e,n,r[n]);if(Le)for(var n of Le(r))Xr.call(r,n)&&Me(e,n,r[n]);return e},Qr=(e,r)=>Kr(e,Ur(r)),Yr=Oe((e,{controlSize:r,controlsOffset:n,orientation:t,height:i,includeGapInSize:s,breakpoints:o=[],slideGap:d})=>{const c=t==="horizontal",u=f=>{if(!s)return{};const v=ie({size:f,sizes:e.spacing});return{[t==="horizontal"?"marginRight":"marginBottom"]:`calc(${v} * -1)`}},a=o.some(f=>typeof f.slideGap<"u"||typeof f.slideSize<"u")?He(e,o).reduce((f,v)=>{const p="maxWidth"in v?"max-width":"min-width",b=ie({size:p==="max-width"?v.maxWidth:v.minWidth,sizes:e.breakpoints}),x=typeof v.slideGap>"u"?void 0:k(v.slideGap),g=qe(b)-(p==="max-width"?1:0);return f[`@media (${p}: ${k(g)})`]=u(x),f},{}):null;return{root:{position:"relative"},viewport:{height:k(i),overflow:"hidden"},container:Ee(Ee({display:"flex",flexDirection:c?"row":"column",height:k(i)},u(d)),a),controls:{position:"absolute",zIndex:1,left:c?0:`calc(50% - ${k(r)} / 2)`,right:c?0:void 0,top:c?`calc(50% - ${k(r)} / 2)`:0,bottom:c?void 0:0,display:"flex",flexDirection:c?"row":"column",alignItems:"center",justifyContent:"space-between",paddingLeft:c?ie({size:n,sizes:e.spacing}):void 0,paddingRight:c?ie({size:n,sizes:e.spacing}):void 0,paddingTop:c?void 0:ie({size:n,sizes:e.spacing}),paddingBottom:c?void 0:ie({size:n,sizes:e.spacing}),pointerEvents:"none"},control:Qr(Ee({display:"flex",justifyContent:"center",alignItems:"center",minWidth:k(r),minHeight:k(r),borderRadius:k(r),pointerEvents:"all",backgroundColor:e.white,color:e.black,boxShadow:e.shadows.md,opacity:e.colorScheme==="dark"?.65:.85,border:`${k(1)} solid ${e.colors.gray[3]}`,transition:`opacity 150ms ${e.transitionTimingFunction}`},e.fn.hover({opacity:1})),{"&:active":e.activeStyles}),indicators:{position:"absolute",bottom:c?e.spacing.md:0,top:c?void 0:0,left:c?0:void 0,right:c?0:e.spacing.md,display:"flex",flexDirection:c?"row":"column",justifyContent:"center",gap:k(8),pointerEvents:"none"},indicator:{pointerEvents:"all",width:c?k(25):k(5),height:c?k(5):k(25),borderRadius:e.radius.xl,backgroundColor:e.white,boxShadow:e.shadows.sm,opacity:.6,transition:`opacity 150ms ${e.transitionTimingFunction}`,"&[data-active]":{opacity:1}}}});const Zr=Yr;var en=Object.defineProperty,je=Object.getOwnPropertySymbols,rn=Object.prototype.hasOwnProperty,nn=Object.prototype.propertyIsEnumerable,$e=(e,r,n)=>r in e?en(e,r,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[r]=n,Pe=(e,r)=>{for(var n in r||(r={}))rn.call(r,n)&&$e(e,n,r[n]);if(je)for(var n of je(r))nn.call(r,n)&&$e(e,n,r[n]);return e},tn=Oe((e,{size:r,gap:n,orientation:t,includeGapInSize:i,breakpoints:s=[]})=>{const o=(u,l)=>{const a=ie({size:u,sizes:e.spacing}),f=k(l),v=i?{[t==="horizontal"?"paddingRight":"paddingBottom"]:a}:{[t==="horizontal"?"marginRight":"marginBottom"]:a};return Pe({flex:`0 0 ${f}`},v)},c=s.some(u=>typeof u.slideGap<"u"||typeof u.slideSize<"u")?He(e,s).reduce((u,l)=>{const a="maxWidth"in l?"max-width":"min-width",f=ie({size:a==="max-width"?l.maxWidth:l.minWidth,sizes:e.breakpoints}),v=typeof l.slideGap>"u"?n:l.slideGap,p=qe(f)-(a==="max-width"?1:0);return u[`@media (${a}: ${k(p)})`]=o(v,l.slideSize),u},{}):null;return{slide:Pe(Pe({position:"relative"},o(n,r)),c)}});const an=tn;var on=Object.defineProperty,he=Object.getOwnPropertySymbols,Ze=Object.prototype.hasOwnProperty,er=Object.prototype.propertyIsEnumerable,Ge=(e,r,n)=>r in e?on(e,r,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[r]=n,sn=(e,r)=>{for(var n in r||(r={}))Ze.call(r,n)&&Ge(e,n,r[n]);if(he)for(var n of he(r))er.call(r,n)&&Ge(e,n,r[n]);return e},ln=(e,r)=>{var n={};for(var t in e)Ze.call(e,t)&&r.indexOf(t)<0&&(n[t]=e[t]);if(e!=null&&he)for(var t of he(e))r.indexOf(t)<0&&er.call(e,t)&&(n[t]=e[t]);return n};const rr=z.forwardRef((e,r)=>{var n=e,{children:t,className:i,size:s,gap:o}=n,d=ln(n,["children","className","size","gap"]);const c=qr(),{classes:u,cx:l}=an({gap:typeof o>"u"?c.slideGap:o,size:typeof s>"u"?c.slideSize:s,orientation:c.orientation,includeGapInSize:c.includeGapInSize,breakpoints:c.breakpoints},{name:"Carousel",classNames:c.classNames,styles:c.styles,unstyled:c.unstyled,variant:c.variant});return X.createElement(We,sn({className:l(u.slide,i),ref:r},d),t)});rr.displayName="@mantine/carousel/CarouselSlide";function Re({dir:e,orientation:r,direction:n}){return n==="previous"?r==="horizontal"?90*(e==="ltr"?1:-1):-180:r==="horizontal"?90*(e==="ltr"?-1:1):0}var cn=Object.defineProperty,Se=Object.getOwnPropertySymbols,nr=Object.prototype.hasOwnProperty,tr=Object.prototype.propertyIsEnumerable,Ve=(e,r,n)=>r in e?cn(e,r,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[r]=n,un=(e,r)=>{for(var n in r||(r={}))nr.call(r,n)&&Ve(e,n,r[n]);if(Se)for(var n of Se(r))tr.call(r,n)&&Ve(e,n,r[n]);return e},dn=(e,r)=>{var n={};for(var t in e)nr.call(e,t)&&r.indexOf(t)<0&&(n[t]=e[t]);if(e!=null&&Se)for(var t of Se(e))r.indexOf(t)<0&&tr.call(e,t)&&(n[t]=e[t]);return n};const fn={controlSize:26,controlsOffset:"sm",slideSize:"100%",slideGap:0,orientation:"horizontal",align:"center",slidesToScroll:1,includeGapInSize:!0,draggable:!0,dragFree:!1,loop:!1,speed:10,initialSlide:0,inViewThreshold:0,withControls:!0,withIndicators:!1,skipSnaps:!1,containScroll:"",withKeyboardEvents:!0},Ne=z.forwardRef((e,r)=>{const n=ir("Carousel",fn,e),{children:t,className:i,getEmblaApi:s,onNextSlide:o,onPreviousSlide:d,onSlideChange:c,nextControlLabel:u,previousControlLabel:l,controlSize:a,controlsOffset:f,classNames:v,styles:p,unstyled:b,slideSize:x,slideGap:g,orientation:m,height:E,align:w,slidesToScroll:y,includeGapInSize:P,draggable:O,dragFree:_,loop:T,speed:H,initialSlide:R,inViewThreshold:Q,withControls:U,withIndicators:W,plugins:G,nextControlIcon:A,previousControlIcon:Z,breakpoints:L,skipSnaps:q,containScroll:Y,withKeyboardEvents:re,variant:ne}=n,te=dn(n,["children","className","getEmblaApi","onNextSlide","onPreviousSlide","onSlideChange","nextControlLabel","previousControlLabel","controlSize","controlsOffset","classNames","styles","unstyled","slideSize","slideGap","orientation","height","align","slidesToScroll","includeGapInSize","draggable","dragFree","loop","speed","initialSlide","inViewThreshold","withControls","withIndicators","plugins","nextControlIcon","previousControlIcon","breakpoints","skipSnaps","containScroll","withKeyboardEvents","variant"]),{classes:M,cx:K,theme:j}=Zr({controlSize:a,controlsOffset:f,orientation:m,height:E,includeGapInSize:P,breakpoints:L,slideGap:g},{name:"Carousel",classNames:v,styles:p,unstyled:b,variant:ne}),[C,h]=ze({axis:m==="horizontal"?"x":"y",direction:m==="horizontal"?j.dir:void 0,startIndex:R,loop:T,align:w,slidesToScroll:y,draggable:O,dragFree:_,speed:H,inViewThreshold:Q,skipSnaps:q,containScroll:Y},G),[B,S]=z.useState(0),[D,V]=z.useState(0),I=z.useCallback(J=>h&&h.scrollTo(J),[h]),$=z.useCallback(()=>{if(!h)return;const J=h.selectedScrollSnap();S(J),c==null||c(J)},[h,S]),ae=z.useCallback(()=>{h==null||h.scrollPrev(),d==null||d()},[h]),fe=z.useCallback(()=>{h==null||h.scrollNext(),o==null||o()},[h]),ve=z.useCallback(J=>{re&&(J.key==="ArrowRight"&&(J.preventDefault(),fe()),J.key==="ArrowLeft"&&(J.preventDefault(),ae()))},[h]);z.useEffect(()=>{if(h)return s==null||s(h),$(),V(h.scrollSnapList().length),h.on("select",$),()=>{h.off("select",$)}},[h,y]),z.useEffect(()=>{h&&(h.reInit(),V(h.scrollSnapList().length),S(J=>or(J,0,z.Children.toArray(t).length-1)))},[z.Children.toArray(t).length,y]);const pe=(h==null?void 0:h.canScrollPrev())||!1,me=(h==null?void 0:h.canScrollNext())||!1,xe=Array(D).fill(0).map((J,we)=>X.createElement(be,{key:we,"data-active":we===B||void 0,className:M.indicator,"aria-hidden":!0,tabIndex:-1,onClick:()=>I(we)}));return X.createElement(Hr,{value:{slideGap:g,slideSize:x,embla:h,orientation:m,includeGapInSize:P,breakpoints:L,classNames:v,styles:p,unstyled:b,variant:ne}},X.createElement(We,un({className:K(M.root,i),ref:r,onKeyDownCapture:ve},te),X.createElement("div",{className:M.viewport,ref:C},X.createElement("div",{className:M.container},t)),W&&X.createElement("div",{className:M.indicators},xe),U&&X.createElement("div",{className:M.controls},X.createElement(be,{onClick:ae,className:M.control,"aria-label":l,"data-inactive":!pe||void 0,tabIndex:pe?0:-1},typeof Z<"u"?Z:X.createElement(Te,{style:{transform:`rotate(${Re({dir:j.dir,orientation:m,direction:"previous"})}deg)`}})),X.createElement(be,{onClick:fe,className:M.control,"aria-label":u,"data-inactive":!me||void 0,tabIndex:me?0:-1},typeof A<"u"?A:X.createElement(Te,{style:{transform:`rotate(${Re({dir:j.dir,orientation:m,direction:"next"})}deg)`}})))))});Ne.Slide=rr;Ne.displayName="@mantine/carousel/Carousel";const Fe=Ne,vn=Oe(e=>({card:{height:k(170),display:"flex",flexDirection:"column",justifyContent:"space-between",alignItems:"flex-start",backgroundSize:"cover",backgroundPosition:"center"},title:{fontWeight:900,color:e.colorScheme==="dark"?e.colors.white:e.colors.dark,lineHeight:1.2,fontSize:k(32),marginTop:0},category:{color:e.colorScheme==="dark"?e.colors.white:e.colors.dark,opacity:.7,fontWeight:700}}));function pn({title:e,description:r,link:n,placeholder:t}){const{classes:i}=vn();return F.jsxs(sr,{shadow:"md",p:"xl",radius:"md",className:i.card,children:[F.jsxs("div",{children:[F.jsxs(Ke,{order:3,className:i.title,children:[e," ",t&&F.jsx(fr,{})]}),F.jsx(lr,{size:"sm",className:i.category,lineClamp:2,children:r})]}),F.jsx(cr,{href:n,target:"_blank",children:F.jsx(ur,{children:F.jsx(Ue,{id:"Qoq+GP"})})})]})}function mn({items:e}){const r=e.map(n=>F.jsx(Fe.Slide,{children:F.jsx(pn,{...n})},n.id));return F.jsx(Fe,{slideSize:"50%",breakpoints:[{maxWidth:"sm",slideSize:"100%",slideGap:k(2)}],slideGap:"xl",align:"start",children:r})}function bn(){return F.jsxs("span",{children:[F.jsx(Ke,{order:5,children:F.jsx(Ue,{id:"7hktsm"})}),F.jsx(mn,{items:dr})]})}export{bn as default};