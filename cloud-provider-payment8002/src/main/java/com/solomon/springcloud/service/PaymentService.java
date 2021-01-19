package com.solomon.springcloud.service;

import com.solomon.springcloud.entities.Payment;

public interface PaymentService {
    public int create(Payment payment);

    public Payment getPaymentById(Long id);
}
