import{G as e,b$ as r,c0 as n}from"./index-9da7d198.js";const{t:o}=e(),a=()=>({required:e=>({required:!0,message:e||o("common.required")}),lengthRange:e=>{const{min:r,max:n,message:a}=e;return{min:r,max:n,message:a||o("common.lengthRange",{min:r,max:n})}},notSpace:e=>({validator:(r,n,a)=>{-1!==(null==n?void 0:n.indexOf(" "))?a(new Error(e||o("common.notSpace"))):a()}}),notSpecialCharacters:e=>({validator:(r,n,a)=>{/[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/gi.test(n)?a(new Error(e||o("common.notSpecialCharacters"))):a()}}),isEmail:(e,o,a)=>{(r(o)||n(o))&&a(),/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(o)?a():a(new Error("请填写正确的邮箱地址"))},isTelephone:(e,o,a)=>{(r(o)||n(o))&&a(),/^1[3-9]\d{9}$/.test(o)?a():a(new Error("请填写正确的手机号"))},isAmount:(e,o,a)=>{(r(o)||n(o))&&a(),/^\d+(\.\d{1,2})?$/.test(o)?a():a(new Error("请填写正确的金额格式"))}});export{a as u};