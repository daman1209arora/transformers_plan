

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on-table b1)
(on b2 b3)
(on b3 b6)
(on-table b4)
(on-table b5)
(on b6 b8)
(on-table b7)
(on b8 b5)
(clear b1)
(clear b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b2 b8)
(on b5 b4)
(on b7 b5)
(on b8 b6))
)
)


