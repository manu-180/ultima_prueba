(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[233],{8971:function(e,t,r){"use strict";r.d(t,{Z:function(){return o}});var n=r(5711);/**
 * @license lucide-react v0.359.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */let o=(0,n.Z)("ChevronDown",[["path",{d:"m6 9 6 6 6-6",key:"qrunsl"}]])},7498:function(e,t){"use strict";var r,n;Object.defineProperty(t,"__esModule",{value:!0}),function(e,t){for(var r in t)Object.defineProperty(e,r,{enumerable:!0,get:t[r]})}(t,{PrefetchKind:function(){return r},ACTION_REFRESH:function(){return o},ACTION_NAVIGATE:function(){return l},ACTION_RESTORE:function(){return u},ACTION_SERVER_PATCH:function(){return f},ACTION_PREFETCH:function(){return i},ACTION_FAST_REFRESH:function(){return a},ACTION_SERVER_ACTION:function(){return c}});let o="refresh",l="navigate",u="restore",f="server-patch",i="prefetch",a="fast-refresh",c="server-action";(n=r||(r={})).AUTO="auto",n.FULL="full",n.TEMPORARY="temporary",("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},30:function(e,t,r){"use strict";function getDomainLocale(e,t,r,n){return!1}Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"getDomainLocale",{enumerable:!0,get:function(){return getDomainLocale}}),r(2866),("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},5170:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"default",{enumerable:!0,get:function(){return _}});let n=r(8754),o=n._(r(7294)),l=r(4450),u=r(2227),f=r(4364),i=r(109),a=r(3607),c=r(1823),s=r(9031),d=r(920),p=r(30),v=r(7192),b=r(7498),h=new Set;function prefetch(e,t,r,n,o,l){if(!l&&!(0,u.isLocalURL)(t))return;if(!n.bypassPrefetchedCheck){let o=void 0!==n.locale?n.locale:"locale"in e?e.locale:void 0,l=t+"%"+r+"%"+o;if(h.has(l))return;h.add(l)}let f=l?e.prefetch(t,o):e.prefetch(t,r,n);Promise.resolve(f).catch(e=>{})}function isModifiedEvent(e){let t=e.currentTarget,r=t.getAttribute("target");return r&&"_self"!==r||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.nativeEvent&&2===e.nativeEvent.which}function linkClicked(e,t,r,n,l,f,i,a,c,s){let{nodeName:d}=e.currentTarget,p="A"===d.toUpperCase();if(p&&(isModifiedEvent(e)||!c&&!(0,u.isLocalURL)(r)))return;e.preventDefault();let navigate=()=>{let e=null==i||i;"beforePopState"in t?t[l?"replace":"push"](r,n,{shallow:f,locale:a,scroll:e}):t[l?"replace":"push"](n||r,{forceOptimisticNavigation:!s,scroll:e})};c?o.default.startTransition(navigate):navigate()}function formatStringOrUrl(e){return"string"==typeof e?e:(0,f.formatUrl)(e)}let y=o.default.forwardRef(function(e,t){let r,n;let{href:u,as:f,children:h,prefetch:y=null,passHref:_,replace:g,shallow:O,scroll:C,locale:m,onClick:E,onMouseEnter:P,onTouchStart:M,legacyBehavior:k=!1,...T}=e;r=h,k&&("string"==typeof r||"number"==typeof r)&&(r=o.default.createElement("a",null,r));let j=o.default.useContext(c.RouterContext),R=o.default.useContext(s.AppRouterContext),A=null!=j?j:R,I=!j,L=!1!==y,S=null===y?b.PrefetchKind.AUTO:b.PrefetchKind.FULL,{href:N,as:U}=o.default.useMemo(()=>{if(!j){let e=formatStringOrUrl(u);return{href:e,as:f?formatStringOrUrl(f):e}}let[e,t]=(0,l.resolveHref)(j,u,!0);return{href:e,as:f?(0,l.resolveHref)(j,f):t||e}},[j,u,f]),x=o.default.useRef(N),w=o.default.useRef(U);k&&(n=o.default.Children.only(r));let D=k?n&&"object"==typeof n&&n.ref:t,[K,F,H]=(0,d.useIntersection)({rootMargin:"200px"}),V=o.default.useCallback(e=>{(w.current!==U||x.current!==N)&&(H(),w.current=U,x.current=N),K(e),D&&("function"==typeof D?D(e):"object"==typeof D&&(D.current=e))},[U,D,N,H,K]);o.default.useEffect(()=>{A&&F&&L&&prefetch(A,N,U,{locale:m},{kind:S},I)},[U,N,F,m,L,null==j?void 0:j.locale,A,I,S]);let q={ref:V,onClick(e){k||"function"!=typeof E||E(e),k&&n.props&&"function"==typeof n.props.onClick&&n.props.onClick(e),A&&!e.defaultPrevented&&linkClicked(e,A,N,U,g,O,C,m,I,L)},onMouseEnter(e){k||"function"!=typeof P||P(e),k&&n.props&&"function"==typeof n.props.onMouseEnter&&n.props.onMouseEnter(e),A&&(L||!I)&&prefetch(A,N,U,{locale:m,priority:!0,bypassPrefetchedCheck:!0},{kind:S},I)},onTouchStart(e){k||"function"!=typeof M||M(e),k&&n.props&&"function"==typeof n.props.onTouchStart&&n.props.onTouchStart(e),A&&(L||!I)&&prefetch(A,N,U,{locale:m,priority:!0,bypassPrefetchedCheck:!0},{kind:S},I)}};if((0,i.isAbsoluteUrl)(U))q.href=U;else if(!k||_||"a"===n.type&&!("href"in n.props)){let e=void 0!==m?m:null==j?void 0:j.locale,t=(null==j?void 0:j.isLocaleDomain)&&(0,p.getDomainLocale)(U,e,null==j?void 0:j.locales,null==j?void 0:j.domainLocales);q.href=t||(0,v.addBasePath)((0,a.addLocale)(U,e,null==j?void 0:j.defaultLocale))}return k?o.default.cloneElement(n,q):o.default.createElement("a",{...T,...q},r)}),_=y;("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},920:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"useIntersection",{enumerable:!0,get:function(){return useIntersection}});let n=r(7294),o=r(3436),l="function"==typeof IntersectionObserver,u=new Map,f=[];function createObserver(e){let t;let r={root:e.root||null,margin:e.rootMargin||""},n=f.find(e=>e.root===r.root&&e.margin===r.margin);if(n&&(t=u.get(n)))return t;let o=new Map,l=new IntersectionObserver(e=>{e.forEach(e=>{let t=o.get(e.target),r=e.isIntersecting||e.intersectionRatio>0;t&&r&&t(r)})},e);return t={id:r,observer:l,elements:o},f.push(r),u.set(r,t),t}function observe(e,t,r){let{id:n,observer:o,elements:l}=createObserver(r);return l.set(e,t),o.observe(e),function(){if(l.delete(e),o.unobserve(e),0===l.size){o.disconnect(),u.delete(n);let e=f.findIndex(e=>e.root===n.root&&e.margin===n.margin);e>-1&&f.splice(e,1)}}}function useIntersection(e){let{rootRef:t,rootMargin:r,disabled:u}=e,f=u||!l,[i,a]=(0,n.useState)(!1),c=(0,n.useRef)(null),s=(0,n.useCallback)(e=>{c.current=e},[]);(0,n.useEffect)(()=>{if(l){if(f||i)return;let e=c.current;if(e&&e.tagName){let n=observe(e,e=>e&&a(e),{root:null==t?void 0:t.current,rootMargin:r});return n}}else if(!i){let e=(0,o.requestIdleCallback)(()=>a(!0));return()=>(0,o.cancelIdleCallback)(e)}},[f,r,t,i,c.current]);let d=(0,n.useCallback)(()=>{a(!1)},[]);return[s,i,d]}("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},1664:function(e,t,r){e.exports=r(5170)}}]);