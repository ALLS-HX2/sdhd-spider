create database SDHD;

use SDHD;

create table song (
    sid integer not null primary key,
    title varchar(100) not null,
    artist varchar(100) not null,
    genre varchar(20) not null,
    version varchar(30) not null,
    bpm integer not null
);

create table songex (
    sid integer not null primary key,
    gameorder integer not null,
    img varchar(20)
);

create view songview as
select song.*, img, gameorder
from song left outer join songex on song.sid = songex.sid
order by gameorder;

create table chart (
    cid integer not null primary key,
    sid integer not null,
    diff integer not null,
    ds decimal(4,1) not null,
    note integer not null,
    designer varchar(50),
    constraint chart_song_fk foreign key (sid) references song(sid)
);

create view songchart as
select songview.*, chart.cid, chart.diff, chart.ds, chart.note, chart.designer
from songview inner join chart on songview.sid = chart.sid
order by gameorder, diff;
