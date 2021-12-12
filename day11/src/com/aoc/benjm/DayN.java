package com.aoc.benjm;

import java.util.*;

public class DayN {
    public long partOne(String filename) {
        return run(filename, false);
    }

    public long partTwo(String filename) {
        return run(filename, true);
    }

    private long run(String filename, boolean isPartTwo) {
        Scanner scanner = new Scanner(DayN.class.getResourceAsStream(filename));
        int h=0;
        int w=0;
        Counter commonCounter = new Counter();
        List<Dumbo> dumbos = new ArrayList<>();
        while (scanner.hasNextLine()) {
            String row = scanner.nextLine();
            if (w==0) w = row.length();
            for (int x = 0; x < row.length(); x++) {
                Dumbo dumbo = new Dumbo(commonCounter, x, h, Integer.valueOf(row.substring(x,x+1)));
                for (Dumbo other : dumbos) {
                    int dx = Math.abs(other.x - dumbo.x);
                    int dy = Math.abs(other.y - dumbo.y);
                    if (dx<2 && dy<2 && dx+dy>0) {
                        dumbo.addNeighbour(other);
                        other.addNeighbour(dumbo);
                    }
                }
                dumbos.add(dumbo);
            }
            h+=1;
        }
        long found = 0;
        int sync = 0;
        //printDumboGrid(h, dumbos, commonCounter.getCounter());
        for (int i = 0; i < 100; i++) {
            for (Dumbo dumbo : dumbos) {
                dumbo.increment();
            }
            for (Dumbo dumbo : dumbos) {
                dumbo.checkFlash();
            }
            sync++;
            int totalPower = dumbos.stream().map(d -> d.getPower()).reduce(0,Integer::sum);
            if (totalPower == 0) {
                found = sync;
            }
            //printDumboGrid(h, dumbos, commonCounter.getCounter());
        }
        if (isPartTwo) {
            while (found < 1) {
                for (Dumbo dumbo : dumbos) {
                    dumbo.increment();
                }
                for (Dumbo dumbo : dumbos) {
                    dumbo.checkFlash();
                }
                sync++;
                int totalPower = dumbos.stream().map(d -> d.getPower()).reduce(0,Integer::sum);
                if (totalPower == 0) {
                    found = sync;
                }
            }
            return found;
        } else {
            return commonCounter.getCounter();
        }
    }

    private void printDumboGrid(int h, List<Dumbo> dumbos, long commonCounter) {
        int n = 0;
        int lineTot = 0;
        int tot = 0;
        for (Dumbo dumbo : dumbos) {
            int p = dumbo.getPower();
            if (p==0) lineTot++;
            if (p < 10) System.out.print(p);
            else System.out.print(".");
            n++;
            if (n % h == 0) {
                System.out.println(" ("+lineTot+")");
                tot+=lineTot;
                lineTot = 0;
            }
        }
        System.out.println("total: "+tot + " and counter: " + commonCounter);
        System.out.println();
    }
}

class Counter {
    private long counter = 0;
    synchronized public void increment() {
        counter++;
    }

    public long getCounter() {
        return counter;
    }
}

class Dumbo {
    public final int x;
    public final int y;
    public final String id;
    private int power;
    private Counter counter;
    private Set<Dumbo> neighbours = new HashSet<>();
    private boolean hasFlashed = false;
    public Dumbo (Counter counter, int x, int y, int power) {
        this.power = power;
        this.x = x;
        this.y = y;
        this.id = x+","+y;
        this.counter = counter;
    }
    public void addNeighbour(Dumbo dumbo) {
        neighbours.add(dumbo);
    }
    public String toString() {
        return id+"=>"+power;
    }
    public String toDetailString() {
        return toString() + " (has" + neighbours.size() + " neighbours)";
    }
    public void increment() {
        power++;
    }
    public void checkFlash() {
        if (power > 9) {
            power = 0;
            counter.increment();
            for (Dumbo d : neighbours) {
                d.flash();
            }
        }
    }
    synchronized public void flash() {
        if (power > 0) { // if it is 0 this dumbo has already flashed
            increment();
            checkFlash();
        }
    }
    public int getPower() {
        return power;
    }
}
