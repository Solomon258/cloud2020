package com.solomon.springcloud.controller;

import com.solomon.springcloud.entities.CommonResult;
import com.solomon.springcloud.entities.Payment;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import javax.annotation.Resource;

@RestController
public class OderController {

    @Resource
    private RestTemplate restTemplate;

    private final static String PAYMENT_URI = "http://localhost:8001";

    @PostMapping("/consumer/create")
    public CommonResult<Payment> create(@RequestBody Payment payment) {
        return restTemplate.postForObject(PAYMENT_URI + "/paymnet/create",payment,CommonResult.class);
    }

    @GetMapping("/consumer/get/{id}")
    public CommonResult<Payment> get(@PathVariable("id") Long id) {
        return restTemplate.getForObject(PAYMENT_URI + "/paymnet/getPaymentById/"+id,  CommonResult.class);
    }
}
