(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[512],{5605:function(e,t,r){(window.__NEXT_P=window.__NEXT_P||[]).push(["/crear_usuario",function(){return r(2131)}])},2131:function(e,t,r){"use strict";r.r(t),r.d(t,{Div_ac2a89ea84667d600a059f034bd91dfe:function(){return Div_ac2a89ea84667d600a059f034bd91dfe},Fragment_cf53a535ae2e610a113dd361eb6ac95b:function(){return Fragment_cf53a535ae2e610a113dd361eb6ac95b},Root_29aa576bc9276dba1116d5585b4d957a:function(){return Root_29aa576bc9276dba1116d5585b4d957a},Submit_549cb47f1596fa8e1a16ce84c72096c7:function(){return Submit_549cb47f1596fa8e1a16ce84c72096c7},Toaster_89416713a273995fc60191a4cf573054:function(){return Toaster_89416713a273995fc60191a4cf573054},default:function(){return Component}});var n=r(2729),a=r(1965),o=r(7294),c=r(687),i=r(6608),s=r(9894),l=r(8971),d=r(917),h=r(4712),u=r(3954),m=r(83),f=r(1664),g=r.n(f),p=r(6822),b=r(9008),C=r.n(b);function _templateObject(){let e=(0,n._)(["\n    0% {\n        opacity: 0;\n    }\n    100% {\n        opacity: 1;\n    }\n"]);return _templateObject=function(){return e},e}function Div_ac2a89ea84667d600a059f034bd91dfe(){let[e,t]=(0,o.useContext)(c.DR);return(0,a.tZ)("div",{css:{position:"fixed",width:"100vw",height:"0"},title:"Connection Error: ".concat(t.length>0?t[t.length-1].message:""),children:(0,a.tZ)(Fragment_cf53a535ae2e610a113dd361eb6ac95b,{})})}function Toaster_89416713a273995fc60191a4cf573054(){let[e,t]=(0,o.useContext)(c.kc);i.xL.__toast=h.A;let[r,n]=(0,o.useContext)(c.DR),s={description:"Check if server is reachable at ".concat((0,i.LH)(u.Ks).href),closeButton:!0,duration:12e4,id:"websocket-error"},[l,d]=(0,o.useState)(!1);return(0,o.useEffect)(()=>{n.length>=2?l||h.A.error("Cannot connect to server: ".concat(n.length>0?n[n.length-1].message:"","."),{...s,onDismiss:()=>d(!0)}):(h.A.dismiss("websocket-error"),d(!1))},[n]),(0,a.tZ)(h.x,{closeButton:!1,expand:!0,position:"bottom-right",richColors:!0,theme:e})}function Submit_549cb47f1596fa8e1a16ce84c72096c7(){let[e,t]=(0,o.useContext)(c.DR),r=(0,o.useCallback)(t=>e([(0,i.ju)("_redirect",{path:"/",external:!1,replace:!1})],t,{}),[e,i.ju]);return(0,a.tZ)(p.k4,{asChild:!0,className:"Submit",onClick:r,children:(0,a.tZ)(m.zx,{css:{width:"100%",height:"100%",padding:"0.5em",borderRadius:"0.8em",whiteSpace:"normal",textAlign:"start","--cursor-button":"pointer",backgroundColor:"#383956","&:hover":{backgroundColor:"#66A9ED"}},type:"submit",children:"Crear usuario"})})}function Root_29aa576bc9276dba1116d5585b4d957a(){let[e,t]=(0,o.useContext)(c.DR),r=(0,o.useCallback)(t=>{let r=t.target;t.preventDefault();let n={...Object.fromEntries(new FormData(r).entries())};e([(0,i.ju)("state.form_state.handle_submit",{form_data:n})]),r.reset()});return(0,a.BX)(p.fC,{className:"Root",css:{width:"100%"},onSubmit:r,children:[(0,a.BX)(p.gN,{className:"Field",css:{display:"grid",marginBottom:"10px"},children:[(0,a.tZ)(p.__,{className:"Label",css:{fontSize:"15px",fontWeight:"500",lineHeight:"35px"},children:"Ingrese su usuario"}),(0,a.tZ)(m.nv.f,{css:{color:"black"},name:"username",placeholder:"Usuario"})]}),(0,a.BX)(p.gN,{className:"Field",css:{display:"grid",marginBottom:"10px"},children:[(0,a.tZ)(p.__,{className:"Label",css:{fontSize:"15px",fontWeight:"500",lineHeight:"35px"},children:"Ingrese su contrase\xf1a"}),(0,a.tZ)(m.nv.f,{css:{color:"black"},name:"password",placeholder:"Contrase\xf1a",type:"password"})]}),(0,a.tZ)(Submit_549cb47f1596fa8e1a16ce84c72096c7,{})]})}let x=(0,d.F4)(_templateObject());function Fragment_cf53a535ae2e610a113dd361eb6ac95b(){let[e,t]=(0,o.useContext)(c.DR);return(0,a.tZ)(o.Fragment,{children:(0,i.oA)(t.length>0)?(0,a.tZ)(o.Fragment,{children:(0,a.tZ)(s.Z,{css:{color:"crimson",zIndex:9999,position:"fixed",bottom:"33px",right:"33px",animation:"".concat(x," 1s infinite")},size:32})}):(0,a.tZ)(o.Fragment,{})})}function Component(){return(0,a.BX)(o.Fragment,{children:[(0,a.BX)(o.Fragment,{children:[(0,a.tZ)(Div_ac2a89ea84667d600a059f034bd91dfe,{}),(0,a.tZ)(Toaster_89416713a273995fc60191a4cf573054,{})]}),(0,a.tZ)(m.xu,{children:(0,a.BX)(m.kC,{align:"center",className:"rx-Stack",css:{width:"100%"},direction:"column",gap:"3",children:[(0,a.tZ)(m.xu,{css:{fontFamily:"Confortaa-Medium","--default-font-family":"Confortaa-Medium",fontSize:"1.3em",position:"sticky",background:"#383956",paddingTop:"0.5em",paddingBottom:"0.5em",paddingInlineStart:"0.5em",paddingInlineEnd:"0.5em",zIndex:"999",top:"0",width:"100%"},children:(0,a.BX)(m.kC,{align:"start",className:"rx-Stack",direction:"row",gap:"3",children:[(0,a.tZ)(m.rU,{asChild:!0,css:{color:"#FCFDFD",textDecoration:"none","&:hover":{color:"var(--accent-8)"}},children:(0,a.tZ)(g(),{href:"/",passHref:!0,children:(0,a.tZ)(m.xv,{as:"p",css:{paddingLeft:"1em"},children:"Taller de ceramica"})})}),(0,a.BX)(m.h_.fC,{css:{marginTop:"0.5em"},children:[(0,a.tZ)(m.h_.xz,{children:(0,a.tZ)(m.zx,{css:{width:"6em",height:"100%",padding:"0.5em",borderRadius:"0.8em",whiteSpace:"normal",textAlign:"start","--cursor-button":"pointer",backgroundColor:"#383956","&:hover":{backgroundColor:"#66A9ED"}},size:"2",variant:"ghost",children:(0,a.tZ)(l.Z,{css:{color:"white"}})})}),(0,a.BX)(m.h_.VY,{children:[(0,a.tZ)(m.rU,{asChild:!0,css:{color:"#FCFDFD",textDecoration:"none","&:hover":{color:"var(--accent-8)"},marginBottom:"0.5em"},children:(0,a.tZ)(g(),{href:"/turnos",passHref:!0,children:(0,a.tZ)(m.zx,{css:{width:"12em",height:"100%",padding:"0.5em",borderRadius:"0.8em",whiteSpace:"normal",textAlign:"start","--cursor-button":"pointer",backgroundColor:"#383956","&:hover":{backgroundColor:"#66A9ED"}},children:(0,a.tZ)(m.xv,{as:"p",children:"turnos"})})})}),(0,a.tZ)(m.rU,{asChild:!0,css:{color:"#FCFDFD",textDecoration:"none","&:hover":{color:"var(--accent-8)"},marginBottom:"2.5em"},children:(0,a.tZ)(g(),{href:"/mis_horarios",passHref:!0,children:(0,a.tZ)(m.zx,{css:{width:"12em",height:"100%",padding:"0.5em",borderRadius:"0.8em",whiteSpace:"normal",textAlign:"start","--cursor-button":"pointer",backgroundColor:"#383956","&:hover":{backgroundColor:"#66A9ED"}},children:(0,a.tZ)(m.xv,{as:"p",children:"mis turnos"})})})})]})]}),(0,a.tZ)(m.kC,{css:{flex:1,justifySelf:"stretch",alignSelf:"stretch"}}),(0,a.tZ)(m.xu,{children:(0,a.tZ)(o.Fragment,{children:(0,i.oA)(!1)?(0,a.tZ)(o.Fragment,{children:(0,a.BX)(m.kC,{align:"start",className:"rx-Stack",css:{width:"100%",alignItems:"end"},direction:"row",gap:"3",children:[(0,a.tZ)(m.kC,{css:{display:"flex",alignItems:"center",justifyContent:"center"},children:(0,a.tZ)(m.rU,{asChild:!0,css:{color:"#FCFDFD",textDecoration:"none","&:hover":{color:"var(--accent-8)"}},children:(0,a.tZ)(g(),{href:"/crear_usuario",passHref:!0,children:(0,a.tZ)(m.zx,{css:{width:"12em",height:"100%",padding:"0.5em",borderRadius:"0.8em",whiteSpace:"normal",textAlign:"start","--cursor-button":"pointer",backgroundColor:"#383956","&:hover":{backgroundColor:"#66A9ED"}},children:(0,a.tZ)(m.xv,{as:"p",children:"Crea tu propio usuario"})})})})}),(0,a.tZ)(m.kC,{css:{display:"flex",alignItems:"center",justifyContent:"center"},children:(0,a.tZ)(m.rU,{asChild:!0,css:{color:"#FCFDFD",textDecoration:"none","&:hover":{color:"var(--accent-8)"}},children:(0,a.tZ)(g(),{href:"/ingreso",passHref:!0,children:(0,a.tZ)(m.zx,{css:{width:"12em",height:"100%",padding:"0.5em",borderRadius:"0.8em",whiteSpace:"normal",textAlign:"start","--cursor-button":"pointer",backgroundColor:"#383956","&:hover":{backgroundColor:"#66A9ED"}},children:(0,a.tZ)(m.xv,{as:"p",children:"iniciar sesion"})})})})})]})}):(0,a.tZ)(o.Fragment,{})})})]})}),(0,a.tZ)(m.X6,{css:{color:"#FCFDFD",fontFamily:"Poppins","--default-font-family":"Poppins",fontWeight:"500"},children:"Crea tu usuario"}),(0,a.tZ)(m.kC,{align:"start",className:"rx-Stack",direction:"column",gap:"3",children:(0,a.tZ)(Root_29aa576bc9276dba1116d5585b4d957a,{})}),(0,a.tZ)(m.kC,{css:{flex:1,justifySelf:"stretch",alignSelf:"stretch"}}),(0,a.tZ)(m.xv,{as:"p",children:"ya tenes un usuario?"}),(0,a.tZ)(m.kC,{css:{display:"flex",alignItems:"center",justifyContent:"center"},children:(0,a.tZ)(m.rU,{asChild:!0,css:{color:"#FCFDFD",textDecoration:"none","&:hover":{color:"var(--accent-8)"}},children:(0,a.tZ)(g(),{href:"/ingreso",passHref:!0,children:(0,a.tZ)(m.zx,{css:{width:"12em",height:"100%",padding:"0.5em",borderRadius:"0.8em",whiteSpace:"normal",textAlign:"start","--cursor-button":"pointer",backgroundColor:"#383956","&:hover":{backgroundColor:"#66A9ED"}},children:(0,a.tZ)(m.xv,{as:"p",children:"iniciar sesion"})})})})})]})}),(0,a.BX)(C(),{children:[(0,a.tZ)("title",{children:"crear usuario"}),(0,a.tZ)("meta",{content:"Taller de ceramica",name:"description"}),(0,a.tZ)("meta",{content:"favicon.ico",property:"og:image"})]})]})}}},function(e){e.O(0,[534,233,822,774,888,179],function(){return e(e.s=5605)}),_N_E=e.O()}]);