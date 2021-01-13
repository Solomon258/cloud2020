package com.solomon.springcloud.controller;

import com.solomon.springcloud.entities.CommonResult;
import com.solomon.springcloud.entities.Payment;
import com.solomon.springcloud.service.PaymentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;

@RestController
@Slf4j
public class PaymentController {

    @Resource
    PaymentService paymentService;

    @PostMapping("/paymnet/create")
    public CommonResult<Payment> create(@RequestBody Payment payment) {
        int count =  paymentService.create(payment);
        if(count > 0){
            return new CommonResult<Payment>("200","插入成功！");
        }else {
            return new CommonResult<Payment>("500","插入失败！");
        }
    }

    @GetMapping("/paymnet/getPaymentById/{id}")
    public CommonResult<Payment> getPaymentById(@PathVariable("id") Long id) {
        Payment payment =  paymentService.getPaymentById(id);
        if(payment == null){
            return new CommonResult<Payment>("200","查询成功！");
        }else {
            return new CommonResult<Payment>("500","查询失败！");
        }
    }
}
