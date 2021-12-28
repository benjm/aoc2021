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
        final List<String> lines = new ArrayList<>();
        while (scanner.hasNextLine()) {
            lines.add(scanner.nextLine());
        }
        final int w = lines.get(0).length();
        final int h = lines.size();
        final Map<String, Pair> pairs = new HashMap<>(w*h);
        for (int x = 0; x < w; x++) {
            for (int y = 0; y < h; y++) {
                final int value = Integer.valueOf(lines.get(y).substring(x,x+1));
                final Pair pair = new Pair(x,y,value);
                pairs.put(pair.id, pair);
            }
        }

        return 0l;

    }
}

class Path {
    private List<Pair> pairs = new ArrayList<>();
    private int total = 0;
    public Path (Pair start) {
        pairs.add(start);
        total+=start.value;
    }
    public
}

class Pair {
    public final int x;
    public final int y;
    public final String id;
    public final int value;

    public Pair(int x, int y, int value) {
        this.x=x;
        this.y=y;
        this.value = value;
        this.id=toid(x,y);
    }

    public static String toid(int x, int y) {
        return x+","+y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Pair pair = (Pair) o;
        return Objects.equals(id, pair.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
