

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b4)
(on b3 b7)
(on-table b4)
(on b5 b8)
(on-table b6)
(on-table b7)
(on b8 b6)
(clear b1)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b7)
(on b3 b8)
(on b5 b3)
(on b6 b5)
(on b7 b2))
)
)


