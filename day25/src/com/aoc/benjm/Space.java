package com.aoc.benjm;

import java.util.Objects;

public class Space {
    public static final char east = '>';
    public static final char south = 'v';
    public static final char empty = '.';
    public final int y;
    public final int x;
    public final String id;
    private char c;
    public final String spaceEastId;
    public final String spaceSouthId;

    public Space(int y, int x, char c, int h, int w) {
        this.y = y;
        this.x = x;
        this.id = xyToId(x,y);
        this.spaceEastId = x+1 >= w ? xyToId(0,y) : xyToId(x+1,y);
        this.spaceSouthId = y+1 >= h ? xyToId(x,0) : xyToId(x,y+1);
        this.c = c;
    }

    public static String xyToId(int x, int y) {
        return "("+x+","+y+")";
    }

    public char getC() {
        return c;
    }

    public void setC(char c) {
        this.c = c;
    }

    @Override
    public String toString() {
        return id + "=" + c;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Space space = (Space) o;
        return Objects.equals(id, space.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
