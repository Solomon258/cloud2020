package com.solomon.springcloud.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CommonResult<T> {

    private String code;

    private String msg;

    private T data;

    public CommonResult(String code,String msg){
        this(code,msg,null);
    }
}
