package com.solomon.springcloud.controller;

import com.netflix.discovery.shared.Applications;
import com.solomon.springcloud.entities.CommonResult;
import com.solomon.springcloud.entities.Payment;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import javax.annotation.Resource;
import java.util.List;

@RestController
@Slf4j
public class OderController {

    @Resource
    private RestTemplate restTemplate;

    @Resource
    private DiscoveryClient discoveryClient;

//    private final static String PAYMENT_URI = "http://localhost:8001";
    private final static String PAYMENT_URI = "http://cloud-payment-service";

    @PostMapping("/consumer/create")
    public CommonResult<Payment> create(@RequestBody Payment payment) {
        return restTemplate.postForObject(PAYMENT_URI + "/paymnet/create",payment,CommonResult.class);
    }

    @GetMapping("/consumer/get/{id}")
    public CommonResult<Payment> get(@PathVariable("id") Long id) {
        return restTemplate.getForObject(PAYMENT_URI + "/paymnet/getPaymentById/"+id,  CommonResult.class);
    }

    @GetMapping("/consumer/discovery/info")
    public Object info() {
        //获取 eureka server 端的所有服务
        List<String> services =  discoveryClient.getServices();
        for (String service :  services) {
            List<ServiceInstance> instances = discoveryClient.getInstances(service);
            log.info("service is {}", service);
            //获取所有实例的信息
            for (ServiceInstance serviceInstance :instances ) {
                log.info("instanceId:{}, serviceId:{}, URI:{}, PORT:{}"
                        , serviceInstance.getInstanceId(), serviceInstance.getServiceId(),serviceInstance.getUri(),serviceInstance.getPort());
            }
        }
        return services;
    }


}
