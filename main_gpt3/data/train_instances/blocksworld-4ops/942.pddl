

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on-table b1)
(on b2 b6)
(on-table b3)
(on b4 b8)
(on b5 b4)
(on-table b6)
(on-table b7)
(on b8 b7)
(clear b1)
(clear b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b8)
(on b2 b6)
(on b3 b1)
(on b6 b3)
(on b8 b5))
)
)


