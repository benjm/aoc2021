package com.aoc.benjm;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class DayNTest {

    @Test
    void partOneExample() {
        long start = System.currentTimeMillis();
        Long l = new DayN().partOne("/testInput.txt");
        log("outp: " + l + "\ntime : " + (System.currentTimeMillis() - start));
        assertEquals(19l, l);
    }

    @Test
    void partOneExample2() {
        long start = System.currentTimeMillis();
        Long l = new DayN().partOne("/testInput2.txt");
        log("outp: " + l + "\ntime : " + (System.currentTimeMillis() - start));
        assertEquals(226l, l);
    }

    @Test
    void partOneFinal() {
        long start = System.currentTimeMillis();
        Long l = new DayN().partOne("/input.txt");
        log("outp: " + l + "\ntime : " + (System.currentTimeMillis() - start));
        assertEquals(5252l, l);
    }

    @Test
    void partTwoExample0() {
        long start = System.currentTimeMillis();
        Long l = new DayN().partTwo("/testInput0.txt");
        log("outp: " + l + "\ntime : " + (System.currentTimeMillis() - start));
        assertEquals(36l, l);
    }

    @Test
    void partTwoExample() {
        long start = System.currentTimeMillis();
        Long l = new DayN().partTwo("/testInput.txt");
        log("outp: " + l + "\ntime : " + (System.currentTimeMillis() - start));
        assertEquals(103l, l);
    }

    @Test
    void partTwoExample2() {
        long start = System.currentTimeMillis();
        Long l = new DayN().partTwo("/testInput2.txt");
        log("outp: " + l + "\ntime : " + (System.currentTimeMillis() - start));
        assertEquals(3509l, l);
    }

    @Test
    void partTwoFinal() {
        long start = System.currentTimeMillis();
        Long l = new DayN().partTwo("/input.txt");
        log("outp: " + l + "\ntime : " + (System.currentTimeMillis() - start));
        assertEquals(147784l, l);
    }

    private static void log(final Object o) {
        System.out.println(o);
    }
}