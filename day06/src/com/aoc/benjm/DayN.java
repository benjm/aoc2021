package com.aoc.benjm;

import java.util.Arrays;
import java.util.Map;
import java.util.Scanner;
import java.util.function.Function;
import java.util.stream.Collectors;

public class DayN {
    public long partOne(String filename) {
        return run(filename, false);
    }

    public long partTwo(String filename) {
        return run(filename, true);
    }

    private long run(String filename, boolean isPartTwo) {
        final int turns = isPartTwo ? 256 : 80;
        Scanner scanner = new Scanner(DayN.class.getResourceAsStream(filename));
        Map<Integer, Long> totals = Arrays.stream(scanner.nextLine().split(","))
                .map(Integer::valueOf)
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
        for (int i = 0; i < turns; i++) {
            long spawn = totals.getOrDefault(0,0l);
            for (int days = 1; days < 9; days++) {
                long tot = totals.getOrDefault(days, 0l);
                totals.put(days-1, tot);
            }
            totals.put(8, spawn);
            totals.put(6, totals.get(6) + spawn);
        }
        sysout("at end: " + totals);
        return totals.values().stream().reduce(0l, (a,b) -> a+b);
    }

    private void sysout(String s) {
        System.out.println(s);
    }
}
