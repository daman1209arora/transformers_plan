

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b4)
(on b3 b6)
(on b4 b7)
(on-table b5)
(on b6 b8)
(on-table b7)
(on-table b8)
(clear b1)
(clear b2)
(clear b5)
)
(:goal
(and
(on b4 b1)
(on b6 b4)
(on b7 b3)
(on b8 b2))
)
)


