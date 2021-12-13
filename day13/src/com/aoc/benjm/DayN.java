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
        Set<Dot> dots = new HashSet<>();
        List<Fold> folds = new ArrayList<>();
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            if (line.startsWith("fold along ")) {
                folds.add(new Fold(line));
            } else if (line.length() > 0) {
                dots.add(new Dot(line));
            }
        }
        Page page = new Page(dots);
        if (isPartTwo) {
            for (Fold fold : folds) {
                page.fold(fold);
            }
            sysout("FINISHING:\n"+page.toString()); // HLBUBGFR
        } else {
            page.fold(folds.get(0));
        }

        return page.countVisibleDots();
    }

    private void sysout(String s) {
        System.out.println(s);
    }
}

class Page {
    private Set<Dot> dots;
    // min & max for folding larger than half... if that happens?
    private int xmin = 0;
    private int xmax = 0;
    private int ymin = 0;
    private int ymax = 0;

    public Page (Set<Dot> dots) {
        this.dots = dots;
        for (Dot dot : dots) {
            if (dot.x > xmax) xmax = dot.x;
            if (dot.y > ymax) ymax = dot.y;
        }
    }

    public void fold(Fold fold) {
        final Set<Dot> newDots = new HashSet<>();
        if (fold.alongX) {
            xmax = fold.position;
            xmin = 0;
        } else {
            ymax = fold.position;
            ymin = 0;
        }
        for (Dot dot : dots) {
            Optional<Dot> newDot = dot.fold(fold);
            if (newDot.isPresent()) {
                newDots.add(newDot.get());
                updateMinMax(newDot.get()); // is this correct? not really sure...
            }
        }
        dots = newDots;
    }

    private void updateMinMax(Dot dot) {
        if (dot.x < xmin) xmin = dot.x;
        if (dot.y < ymin) ymin = dot.y;
        if (dot.x > xmax) xmax = dot.x;
        if (dot.y > ymax) ymax = dot.y;
    }

    public long countVisibleDots() {
        return dots.size();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int y = ymin; y < ymax; y++) {
            for (int x = xmin; x < xmax; x++) {
                Dot d = new Dot(x, y);
                char c = dots.contains(d) ? '#' : '.';
                sb.append(c);
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}

class Dot {
    final public int x;
    final public int y;
    final public String id;
    public Dot(String input) {
        id=input;
        String[] lr = input.split(",");
        x = Integer.valueOf(lr[0]);
        y = Integer.valueOf(lr[1]);
    }
    public Dot(int x, int y) {
        id = x+","+y;
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString() {
        return id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Dot dot = (Dot) o;
        return id.equals(dot.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    public Optional<Dot> fold(Fold fold) {
        //account for negatives?
        final int p = fold.position;
        if (fold.alongX) {
            if (p == x) return Optional.empty();
            final int xNew = x < p ? x : p - (x - p);
            return Optional.of(new Dot(xNew, y));
        } else {
            if (p == y) return Optional.empty();
            final int yNew = y < p ? y : p - (y - p);
            return Optional.of(new Dot(x, yNew));
        }
    }
}

class Fold {
    final public int position;
    final public boolean alongX;
    final public String id;
    public Fold(String line) {
        String fold = line.substring(11);
        String[] lr = fold.split("=");
        alongX = lr[0].equals("x");
        position = Integer.valueOf(lr[1]);
        id=fold;
    }

    @Override
    public String toString() {
        return id;
    }
}
